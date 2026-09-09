import pytest
from fastapi.testclient import TestClient
from main import app
from db_connection import get_tasks_collection, get_users_collection
from bson import ObjectId
from datetime import datetime, timezone
import auth

client = TestClient(app, follow_redirects=False)

def test_unauthenticated_access_redirects_to_login():
    """Verify unauthenticated access to / redirects to /login."""
    response = client.get("/")
    assert response.status_code == 303
    assert response.headers["location"] == "/login"


def test_unauthenticated_api_returns_401():
    """Verify unauthenticated REST API requests are rejected with 401."""
    resp_tasks = client.get("/api/tasks")
    assert resp_tasks.status_code == 401

    resp_streak = client.get("/api/stats/streak")
    assert resp_streak.status_code == 401

    resp_create = client.post("/api/tasks", json={"task": "Unauthorized Task"})
    assert resp_create.status_code == 401


def test_user_a_and_user_b_isolation_lifecycle():
    """
    Complete multi-user lifecycle test:
    1. Account A logs in and creates tasks.
    2. Account B logs in and cannot see Account A's tasks.
    3. Account B creates tasks.
    4. Account B cannot edit, toggle, or delete Account A's tasks.
    5. Account A logs in, verifies its tasks are intact, and cannot see Account B's tasks.
    6. Logout properly invalidates session.
    """
    # 1. Login as Account A
    login_a_resp = client.get("/auth/dev-login?account=user_a")
    assert login_a_resp.status_code == 303
    session_a = login_a_resp.cookies.get(auth.SESSION_COOKIE_NAME)
    assert session_a is not None

    cookies_a = {auth.SESSION_COOKIE_NAME: session_a}

    # Verify Dashboard accessible for Account A
    dash_a = client.get("/", cookies=cookies_a)
    assert dash_a.status_code == 200
    assert "Alex" in dash_a.text

    # Account A creates Task A1
    create_a1_resp = client.post(
        "/api/tasks",
        json={"task": "Account A Confidential Task 1", "priority": "High", "category": "Work"},
        cookies=cookies_a
    )
    assert create_a1_resp.status_code == 200
    task_a1_id = create_a1_resp.json()["id"]

    # Account A creates Task A2
    create_a2_resp = client.post(
        "/api/tasks",
        json={"task": "Account A Second Task", "priority": "Medium", "category": "Personal"},
        cookies=cookies_a
    )
    assert create_a2_resp.status_code == 200
    task_a2_id = create_a2_resp.json()["id"]

    # Verify Account A sees its tasks
    tasks_a = client.get("/api/tasks", cookies=cookies_a).json()
    task_a_ids = [t["id"] for t in tasks_a["tasks"]]
    assert task_a1_id in task_a_ids
    assert task_a2_id in task_a_ids

    # 2. Login as Account B
    login_b_resp = client.get("/auth/dev-login?account=user_b")
    assert login_b_resp.status_code == 303
    session_b = login_b_resp.cookies.get(auth.SESSION_COOKIE_NAME)
    assert session_b is not None
    assert session_b != session_a

    cookies_b = {auth.SESSION_COOKIE_NAME: session_b}

    # Verify Dashboard accessible for Account B
    dash_b = client.get("/", cookies=cookies_b)
    assert dash_b.status_code == 200
    assert "Beatriz" in dash_b.text

    # Verify Account B DOES NOT see Account A's tasks
    tasks_b_initial = client.get("/api/tasks", cookies=cookies_b).json()
    task_b_initial_ids = [t["id"] for t in tasks_b_initial["tasks"]]
    assert task_a1_id not in task_b_initial_ids
    assert task_a2_id not in task_b_initial_ids

    # 3. Account B creates Task B1
    create_b1_resp = client.post(
        "/api/tasks",
        json={"task": "Account B Private Goal", "priority": "Low", "category": "Study"},
        cookies=cookies_b
    )
    assert create_b1_resp.status_code == 200
    task_b1_id = create_b1_resp.json()["id"]

    # Verify Account B only sees Task B1
    tasks_b = client.get("/api/tasks", cookies=cookies_b).json()
    task_b_ids = [t["id"] for t in tasks_b["tasks"]]
    assert task_b1_id in task_b_ids
    assert task_a1_id not in task_b_ids

    # 4. Account B attempts cross-user unauthorized operations on Account A's task
    # Edit attempt
    hack_edit = client.put(
        f"/api/tasks/{task_a1_id}",
        json={"task_title": "Hacked Title by User B"},
        cookies=cookies_b
    )
    assert hack_edit.status_code == 404

    # Toggle attempt
    hack_toggle = client.post(f"/api/tasks/{task_a1_id}/toggle", cookies=cookies_b)
    assert hack_toggle.status_code == 404

    # Delete attempt
    hack_delete = client.delete(f"/api/tasks/{task_a1_id}", cookies=cookies_b)
    assert hack_delete.status_code == 404

    # 5. Account A logs in again / makes requests
    tasks_a_after = client.get("/api/tasks", cookies=cookies_a).json()
    task_a_after_ids = [t["id"] for t in tasks_a_after["tasks"]]
    assert task_a1_id in task_a_after_ids
    assert task_a2_id in task_a_after_ids
    assert task_b1_id not in task_a_after_ids

    # Verify Account A1 task content was NOT tampered by User B
    a1_task = next(t for t in tasks_a_after["tasks"] if t["id"] == task_a1_id)
    assert a1_task["task_title"] == "Account A Confidential Task 1"

    # Account A updates and toggles its own task
    update_a1 = client.put(
        f"/api/tasks/{task_a1_id}",
        json={"task_title": "Account A Updated Task 1"},
        cookies=cookies_a
    )
    assert update_a1.status_code == 200

    toggle_a1 = client.post(f"/api/tasks/{task_a1_id}/toggle", cookies=cookies_a)
    assert toggle_a1.status_code == 200
    assert toggle_a1.json()["completed"] is True

    # Account A deletes its task A2
    del_a2 = client.delete(f"/api/tasks/{task_a2_id}", cookies=cookies_a)
    assert del_a2.status_code == 200

    # Clean up test task A1 and B1
    client.delete(f"/api/tasks/{task_a1_id}", cookies=cookies_a)
    client.delete(f"/api/tasks/{task_b1_id}", cookies=cookies_b)

    # 6. Test Logout
    logout_resp = client.get("/auth/logout", cookies=cookies_a)
    assert logout_resp.status_code == 303
    assert "/login" in logout_resp.headers["location"]


def test_bulk_save_isolation():
    """Verify POST /api/tasks/save preserves user isolation."""
    login_a = client.get("/auth/dev-login?account=user_a")
    cookies_a = {auth.SESSION_COOKIE_NAME: login_a.cookies.get(auth.SESSION_COOKIE_NAME)}

    login_b = client.get("/auth/dev-login?account=user_b")
    cookies_b = {auth.SESSION_COOKIE_NAME: login_b.cookies.get(auth.SESSION_COOKIE_NAME)}

    # User A saves tasks for date 2026-10-15
    save_resp_a = client.post(
        "/api/tasks/save",
        json={
            "date": "2026-10-15",
            "tasks": [
                {"task_title": "Task A1 for Oct 15", "priority": "High", "completed": False, "category": "Work"},
                {"task_title": "Task A2 for Oct 15", "priority": "Low", "completed": True, "category": "General"}
            ]
        },
        cookies=cookies_a
    )
    assert save_resp_a.status_code == 200
    assert save_resp_a.json()["total_count"] == 2

    # User B checks date 2026-10-15 -> must be 0 tasks
    tasks_b = client.get("/api/tasks?date=2026-10-15", cookies=cookies_b).json()
    assert tasks_b["total_count"] == 0
    assert len(tasks_b["tasks"]) == 0

    # User B saves a task for same date
    save_resp_b = client.post(
        "/api/tasks/save",
        json={
            "date": "2026-10-15",
            "tasks": [
                {"task_title": "Task B1 for Oct 15", "priority": "Medium", "completed": True, "category": "Study"}
            ]
        },
        cookies=cookies_b
    )
    assert save_resp_b.status_code == 200
    assert save_resp_b.json()["total_count"] == 1

    # User A checks again -> still exactly 2 tasks
    tasks_a = client.get("/api/tasks?date=2026-10-15", cookies=cookies_a).json()
    assert tasks_a["total_count"] == 2
    a_titles = [t["task_title"] for t in tasks_a["tasks"]]
    assert "Task A1 for Oct 15" in a_titles
    assert "Task A2 for Oct 15" in a_titles
    assert "Task B1 for Oct 15" not in a_titles

    # Clean up Oct 15 tasks
    client.post("/api/tasks/save", json={"date": "2026-10-15", "tasks": []}, cookies=cookies_a)
    client.post("/api/tasks/save", json={"date": "2026-10-15", "tasks": []}, cookies=cookies_b)


def test_unowned_existing_tasks_safety():
    """Verify tasks without owner (legacy data) are NOT exposed to any authenticated user."""
    tasks_col = get_tasks_collection()
    inserted = tasks_col.insert_one({
        "task_title": "Orphaned Unowned Legacy Task",
        "status": "Pending",
        "completed": False,
        "priority": "Medium",
        "category": "General",
        "date": "2026-11-01",
        "created_at": datetime.now(timezone.utc)
    })
    orphan_id = inserted.inserted_id

    # User A queries
    login_a = client.get("/auth/dev-login?account=user_a")
    cookies_a = {auth.SESSION_COOKIE_NAME: login_a.cookies.get(auth.SESSION_COOKIE_NAME)}

    tasks_resp = client.get("/api/tasks?date=2026-11-01", cookies=cookies_a).json()
    task_ids = [t["id"] for t in tasks_resp["tasks"]]
    assert str(orphan_id) not in task_ids

    # Clean up orphan
    tasks_col.delete_one({"_id": orphan_id})


def test_google_auth_endpoint_redirection():
    """Test /auth/google behavior."""
    resp = client.get("/auth/google")
    assert resp.status_code == 303
    if auth.is_google_auth_configured():
        assert "accounts.google.com" in resp.headers["location"]
        assert "client_id=" in resp.headers["location"]
        assert "response_type=code" in resp.headers["location"]
    else:
        assert "login" in resp.headers["location"]


def test_login_page_renders():
    """Test that login page renders with HTTP 200 and expected markup when unauthenticated."""
    fresh_client = TestClient(app, follow_redirects=False)
    resp = fresh_client.get("/login")
    assert resp.status_code == 200
    assert "TaskMaster" in resp.text
    assert "Sign In" in resp.text or "Welcome back" in resp.text


def test_custom_account_dev_login():
    """Test dev login with a custom user identifier."""
    resp = client.get("/auth/dev-login?account=sarah.connor@example.com&name=Sarah")
    assert resp.status_code == 303
    token = resp.cookies.get(auth.SESSION_COOKIE_NAME)
    assert token is not None
    user = auth.decode_session_token(token)
    assert user["name"] == "Sarah"
    assert user["email"] == "sarah.connor@example.com"

