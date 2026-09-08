from fastapi import FastAPI, Request, Form, Query, HTTPException, Body
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId
from db_connection import get_tasks_collection
from datetime import datetime, timezone, timedelta
import os
import re

app = FastAPI(title="TaskMaster Todo App")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")

VALID_CATEGORIES = ["General", "Work", "Personal", "Study", "Health", "Finance"]
VALID_PRIORITIES = ["High", "Medium", "Low"]


def get_today_date_str() -> str:
    """Returns the current date in YYYY-MM-DD format (UTC)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def is_valid_date(date_str: str) -> bool:
    """Validates YYYY-MM-DD date format."""
    if not date_str or not DATE_REGEX.match(date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def normalize_task_doc(doc: dict, target_date: str = None) -> dict:
    """Standardizes MongoDB task document into a consistent structure."""
    task_id = str(doc.get("_id", ""))
    task_title = doc.get("task_title") or doc.get("task") or ""
    status = doc.get("status", "Pending")
    
    # Handle boolean or string completion status
    if "completed" in doc and isinstance(doc["completed"], bool):
        completed = doc["completed"]
        status = "Completed" if completed else "Pending"
    else:
        completed = (status == "Completed")
        status = "Completed" if completed else "Pending"

    priority = doc.get("priority", "Medium")
    if priority not in VALID_PRIORITIES:
        priority = "Medium"

    category = doc.get("category", "General")
    if category not in VALID_CATEGORIES:
        category = "General"

    notes = doc.get("notes", "") or ""
    order = doc.get("order", 0)
    try:
        order = int(order)
    except (ValueError, TypeError):
        order = 0
    
    # Determine date
    task_date = doc.get("date")
    if not task_date:
        created_at = doc.get("created_at")
        if isinstance(created_at, datetime):
            task_date = created_at.strftime("%Y-%m-%d")
        else:
            task_date = target_date or get_today_date_str()

    created_at = doc.get("created_at")
    created_at_val = created_at.isoformat() if isinstance(created_at, datetime) else (str(created_at) if created_at else None)

    updated_at = doc.get("updated_at")
    updated_at_val = updated_at.isoformat() if isinstance(updated_at, datetime) else (str(updated_at) if updated_at else None)

    return {
        "id": task_id,
        "task_title": task_title,
        "status": status,
        "completed": completed,
        "priority": priority,
        "category": category,
        "notes": notes,
        "order": order,
        "date": task_date,
        "created_at": created_at_val,
        "updated_at": updated_at_val
    }


def fetch_tasks_for_date(date_str: str):
    """Fetches and computes statistics for tasks on a given date."""
    tasks_collection = get_tasks_collection()
    
    try:
        dt_start = datetime.strptime(date_str, "%Y-%m-%d")
        dt_end = dt_start.replace(hour=23, minute=59, second=59, microsecond=999999)
    except Exception:
        dt_start = None
        dt_end = None

    query = {
        "$or": [
            {"date": date_str}
        ]
    }
    if dt_start and dt_end:
        query["$or"].append({
            "date": {"$exists": False},
            "created_at": {"$gte": dt_start, "$lte": dt_end}
        })
        query["$or"].append({
            "date": None,
            "created_at": {"$gte": dt_start, "$lte": dt_end}
        })

    # Sort by order ascending, then _id descending
    raw_tasks = list(tasks_collection.find(query).sort([("order", 1), ("_id", -1)]))
    
    tasks = []
    completed_count = 0
    pending_count = 0

    for doc in raw_tasks:
        norm = normalize_task_doc(doc, target_date=date_str)
        tasks.append(norm)
        if norm["status"] == "Completed":
            completed_count += 1
        else:
            pending_count += 1

    total_count = len(tasks)
    progress_percentage = round((completed_count / total_count) * 100) if total_count > 0 else 0

    return {
        "date": date_str,
        "tasks": tasks,
        "total_count": total_count,
        "completed_count": completed_count,
        "pending_count": pending_count,
        "progress_percentage": progress_percentage
    }


def calculate_user_streak():
    """Computes current streak of consecutive days with completed tasks and 7-day activity."""
    tasks_collection = get_tasks_collection()
    now_utc = datetime.now(timezone.utc)
    today_date = now_utc.date()

    # Find distinct dates with at least one completed task
    completed_tasks = list(tasks_collection.find(
        {"$or": [{"status": "Completed"}, {"completed": True}]},
        {"date": 1, "created_at": 1}
    ))

    completed_dates = set()
    for doc in completed_tasks:
        d_str = doc.get("date")
        if d_str and is_valid_date(d_str):
            completed_dates.add(d_str)
        elif isinstance(doc.get("created_at"), datetime):
            completed_dates.add(doc["created_at"].strftime("%Y-%m-%d"))

    # Calculate streak (counting backwards from today or yesterday)
    streak = 0
    check_date = today_date
    today_str = today_date.strftime("%Y-%m-%d")

    # If today has completed tasks, streak starts from today
    # Otherwise check if yesterday had completed tasks to keep the streak alive
    if today_str in completed_dates:
        streak += 1
        check_date = check_date - timedelta(days=1)
    else:
        yesterday_str = (today_date - timedelta(days=1)).strftime("%Y-%m-%d")
        if yesterday_str in completed_dates:
            check_date = today_date - timedelta(days=1)
        else:
            check_date = None

    while check_date is not None:
        c_str = check_date.strftime("%Y-%m-%d")
        if c_str in completed_dates:
            streak += 1
            check_date = check_date - timedelta(days=1)
        else:
            break

    # Build 7-day mini heatmap (last 7 days ending today) in a single fast batched query
    seven_day_dates = [(today_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    start_dt = datetime.strptime(seven_day_dates[0], "%Y-%m-%d")
    end_dt = datetime.strptime(seven_day_dates[-1], "%Y-%m-%d").replace(hour=23, minute=59, second=59, microsecond=999999)

    recent_docs = list(tasks_collection.find({
        "$or": [
            {"date": {"$in": seven_day_dates}},
            {"date": None, "created_at": {"$gte": start_dt, "$lte": end_dt}},
            {"date": {"$exists": False}, "created_at": {"$gte": start_dt, "$lte": end_dt}}
        ]
    }))

    # Aggregate counts by date in memory
    day_stats = {d: {"total": 0, "completed": 0} for d in seven_day_dates}
    for doc in recent_docs:
        norm = normalize_task_doc(doc)
        d = norm["date"]
        if d in day_stats:
            day_stats[d]["total"] += 1
            if norm["status"] == "Completed":
                day_stats[d]["completed"] += 1

    heatmap = []
    for day_str in seven_day_dates:
        day_obj = datetime.strptime(day_str, "%Y-%m-%d")
        day_name = day_obj.strftime("%a") # e.g. Mon, Tue
        day_number = day_obj.strftime("%d")

        t_count = day_stats[day_str]["total"]
        c_count = day_stats[day_str]["completed"]

        heatmap.append({
            "date": day_str,
            "day_name": day_name,
            "day_number": day_number,
            "is_today": (day_str == today_str),
            "total_count": t_count,
            "completed_count": c_count,
            "has_activity": (c_count > 0),
            "all_completed": (t_count > 0 and c_count == t_count)
        })

    return {
        "streak": streak,
        "heatmap": heatmap
    }


# ---------------- Pydantic Request Models ----------------

class TaskItemPayload(BaseModel):
    id: Optional[str] = None
    task_title: str
    status: Optional[str] = "Pending"
    completed: Optional[bool] = False
    priority: Optional[str] = "Medium"
    category: Optional[str] = "General"
    notes: Optional[str] = ""
    order: Optional[int] = 0
    date: Optional[str] = None


class SaveDayTasksRequest(BaseModel):
    date: str
    tasks: List[TaskItemPayload]


class CreateTaskRequest(BaseModel):
    task: str
    priority: Optional[str] = "Medium"
    category: Optional[str] = "General"
    notes: Optional[str] = ""
    date: Optional[str] = None


class UpdateTaskRequest(BaseModel):
    task_title: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None
    completed: Optional[bool] = None
    order: Optional[int] = None


# ---------------- Web Routes (HTML) ----------------

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    favicon_path = os.path.join("static", "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    return HTMLResponse(status_code=404)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, date: Optional[str] = None):
    error_message = None
    selected_date = date if (date and is_valid_date(date)) else get_today_date_str()
    tasks_data = {
        "date": selected_date,
        "tasks": [],
        "total_count": 0,
        "completed_count": 0,
        "pending_count": 0,
        "progress_percentage": 0
    }
    streak_data = {"streak": 0, "heatmap": []}

    try:
        tasks_data = fetch_tasks_for_date(selected_date)
        streak_data = calculate_user_streak()
    except Exception as e:
        error_message = (
            "Could not connect to MongoDB. Please ensure your MongoDB credentials "
            "and network access (0.0.0.0/0 IP whitelist) are configured."
        )
        print(f"Database connection error: {e}")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": tasks_data["tasks"],
            "selected_date": selected_date,
            "error": error_message,
            "total_count": tasks_data["total_count"],
            "completed_count": tasks_data["completed_count"],
            "pending_count": tasks_data["pending_count"],
            "progress_percentage": tasks_data["progress_percentage"],
            "streak": streak_data["streak"],
            "heatmap": streak_data["heatmap"]
        }
    )


# ---------------- REST API Endpoints ----------------

@app.get("/api/tasks")
def get_tasks_api(date: Optional[str] = Query(None)):
    """Fetch all tasks and statistics for a specific date (YYYY-MM-DD)."""
    selected_date = date if (date and is_valid_date(date)) else get_today_date_str()
    try:
        data = fetch_tasks_for_date(selected_date)
        return data
    except Exception as e:
        print(f"API Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch tasks: {str(e)}")


@app.get("/api/stats/streak")
def get_streak_api():
    """Fetch user daily streak and 7-day activity heatmap."""
    try:
        return calculate_user_streak()
    except Exception as e:
        print(f"API Error fetching streak: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch streak: {str(e)}")


@app.post("/api/tasks/save")
def save_day_tasks_api(payload: SaveDayTasksRequest):
    """
    Saves all tasks for a specific date in one request, preserving ordering, categories, and notes.
    Existing tasks for other dates are NEVER touched.
    """
    date_str = payload.date.strip()
    if not is_valid_date(date_str):
        raise HTTPException(status_code=400, detail="Invalid date format. Expected YYYY-MM-DD.")

    try:
        tasks_collection = get_tasks_collection()
        now = datetime.now(timezone.utc)
        kept_object_ids = []

        for index, item in enumerate(payload.tasks):
            title = item.task_title.strip()
            if not title:
                continue

            status = "Completed" if (item.completed or item.status == "Completed") else "Pending"
            priority = item.priority if item.priority in VALID_PRIORITIES else "Medium"
            category = item.category if item.category in VALID_CATEGORIES else "General"
            notes = item.notes.strip() if item.notes else ""
            order = item.order if item.order is not None else index
            completed = (status == "Completed")

            doc_id = None
            if item.id and ObjectId.is_valid(item.id):
                doc_id = ObjectId(item.id)

            if doc_id:
                tasks_collection.update_one(
                    {"_id": doc_id},
                    {
                        "$set": {
                            "task_title": title,
                            "status": status,
                            "completed": completed,
                            "priority": priority,
                            "category": category,
                            "notes": notes,
                            "order": order,
                            "date": date_str,
                            "updated_at": now
                        }
                    }
                )
                kept_object_ids.append(doc_id)
            else:
                result = tasks_collection.insert_one({
                    "task_title": title,
                    "status": status,
                    "completed": completed,
                    "priority": priority,
                    "category": category,
                    "notes": notes,
                    "order": order,
                    "date": date_str,
                    "created_at": now,
                    "updated_at": now
                })
                kept_object_ids.append(result.inserted_id)

        # Delete any tasks that belonged to this specific date but were removed in this save
        try:
            dt_start = datetime.strptime(date_str, "%Y-%m-%d")
            dt_end = dt_start.replace(hour=23, minute=59, second=59, microsecond=999999)
        except Exception:
            dt_start = None
            dt_end = None

        date_match_conditions = [{"date": date_str}]
        if dt_start and dt_end:
            date_match_conditions.append({
                "date": {"$exists": False},
                "created_at": {"$gte": dt_start, "$lte": dt_end}
            })
            date_match_conditions.append({
                "date": None,
                "created_at": {"$gte": dt_start, "$lte": dt_end}
            })

        delete_query = {
            "$and": [
                {"$or": date_match_conditions},
                {"_id": {"$nin": kept_object_ids}}
            ]
        }
        tasks_collection.delete_many(delete_query)

        updated_data = fetch_tasks_for_date(date_str)
        streak_data = calculate_user_streak()
        return {
            "success": True,
            "message": "Tasks saved successfully!",
            **updated_data,
            "streak": streak_data["streak"],
            "heatmap": streak_data["heatmap"]
        }
    except Exception as e:
        print(f"API Error saving tasks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save tasks: {str(e)}")


@app.post("/api/tasks")
def create_task_api(payload: CreateTaskRequest):
    """Add a single task for a specific date."""
    task_text = payload.task.strip()
    if not task_text:
        raise HTTPException(status_code=400, detail="Task title cannot be empty.")

    target_date = payload.date if (payload.date and is_valid_date(payload.date)) else get_today_date_str()
    priority = payload.priority if payload.priority in VALID_PRIORITIES else "Medium"
    category = payload.category if payload.category in VALID_CATEGORIES else "General"
    notes = payload.notes.strip() if payload.notes else ""
    now = datetime.now(timezone.utc)

    try:
        tasks_collection = get_tasks_collection()
        result = tasks_collection.insert_one({
            "task_title": task_text,
            "status": "Pending",
            "completed": False,
            "priority": priority,
            "category": category,
            "notes": notes,
            "order": 0,
            "date": target_date,
            "created_at": now,
            "updated_at": now
        })

        return {
            "success": True,
            "id": str(result.inserted_id),
            "task_title": task_text,
            "status": "Pending",
            "completed": False,
            "priority": priority,
            "category": category,
            "notes": notes,
            "order": 0,
            "date": target_date
        }
    except Exception as e:
        print(f"API Error creating task: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@app.put("/api/tasks/{task_id}")
def update_task_api(task_id: str, payload: UpdateTaskRequest):
    """Update task title, priority, category, notes, or status."""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID.")

    update_fields = {"updated_at": datetime.now(timezone.utc)}
    if payload.task_title is not None:
        title = payload.task_title.strip()
        if title:
            update_fields["task_title"] = title
    if payload.priority is not None and payload.priority in VALID_PRIORITIES:
        update_fields["priority"] = payload.priority
    if payload.category is not None and payload.category in VALID_CATEGORIES:
        update_fields["category"] = payload.category
    if payload.notes is not None:
        update_fields["notes"] = payload.notes.strip()
    if payload.order is not None:
        update_fields["order"] = int(payload.order)
    if payload.completed is not None:
        update_fields["completed"] = payload.completed
        update_fields["status"] = "Completed" if payload.completed else "Pending"
    elif payload.status is not None:
        update_fields["status"] = payload.status
        update_fields["completed"] = (payload.status == "Completed")

    try:
        tasks_collection = get_tasks_collection()
        res = tasks_collection.update_one({"_id": ObjectId(task_id)}, {"$set": update_fields})
        if res.matched_count == 0:
            raise HTTPException(status_code=404, detail="Task not found.")
        return {"success": True, "message": "Task updated successfully."}
    except HTTPException:
        raise
    except Exception as e:
        print(f"API Error updating task: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@app.post("/api/tasks/{task_id}/toggle")
def toggle_task_api(task_id: str):
    """Toggle task status between Pending and Completed."""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID.")

    try:
        tasks_collection = get_tasks_collection()
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found.")

        new_status = "Pending" if task.get("status") == "Completed" else "Completed"
        new_completed = (new_status == "Completed")
        tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": new_status, "completed": new_completed, "updated_at": datetime.now(timezone.utc)}}
        )
        return {"success": True, "id": task_id, "status": new_status, "completed": new_completed}
    except HTTPException:
        raise
    except Exception as e:
        print(f"API Error toggling task: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to toggle task: {str(e)}")


@app.delete("/api/tasks/{task_id}")
def delete_task_api(task_id: str):
    """Delete a task by ID."""
    if not ObjectId.is_valid(task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID.")

    try:
        tasks_collection = get_tasks_collection()
        res = tasks_collection.delete_one({"_id": ObjectId(task_id)})
        if res.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found.")
        return {"success": True, "message": "Task deleted successfully."}
    except HTTPException:
        raise
    except Exception as e:
        print(f"API Error deleting task: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


# ---------------- Legacy Form Submission Support ----------------

@app.post("/add")
def add_task_form(
    task: str = Form(...),
    priority: str = Form("Medium"),
    category: str = Form("General"),
    date: Optional[str] = Form(None)
):
    target_date = date if (date and is_valid_date(date)) else get_today_date_str()
    task_text = task.strip()
    if task_text:
        try:
            tasks_collection = get_tasks_collection()
            now = datetime.now(timezone.utc)
            tasks_collection.insert_one({
                "task_title": task_text,
                "status": "Pending",
                "completed": False,
                "priority": priority if priority in VALID_PRIORITIES else "Medium",
                "category": category if category in VALID_CATEGORIES else "General",
                "notes": "",
                "order": 0,
                "date": target_date,
                "created_at": now,
                "updated_at": now
            })
        except Exception as e:
            print(f"Error adding task: {e}")

    return RedirectResponse(f"/?date={target_date}", status_code=303)


@app.get("/toggle/{task_id}")
def toggle_task_form(task_id: str, date: Optional[str] = Query(None)):
    target_date = date if (date and is_valid_date(date)) else get_today_date_str()
    try:
        if ObjectId.is_valid(task_id):
            tasks_collection = get_tasks_collection()
            task = tasks_collection.find_one({"_id": ObjectId(task_id)})
            if task:
                new_status = "Pending" if task.get("status") == "Completed" else "Completed"
                new_completed = (new_status == "Completed")
                tasks_collection.update_one(
                    {"_id": ObjectId(task_id)},
                    {"$set": {"status": new_status, "completed": new_completed, "updated_at": datetime.now(timezone.utc)}}
                )
    except Exception as e:
        print(f"Error toggling task: {e}")

    return RedirectResponse(f"/?date={target_date}", status_code=303)


@app.get("/complete/{task_id}")
def complete_task_form(task_id: str, date: Optional[str] = Query(None)):
    target_date = date if (date and is_valid_date(date)) else get_today_date_str()
    try:
        if ObjectId.is_valid(task_id):
            tasks_collection = get_tasks_collection()
            tasks_collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {"status": "Completed", "completed": True, "updated_at": datetime.now(timezone.utc)}}
            )
    except Exception as e:
        print(f"Error completing task: {e}")

    return RedirectResponse(f"/?date={target_date}", status_code=303)


@app.get("/delete/{task_id}")
def delete_task_form(task_id: str, date: Optional[str] = Query(None)):
    target_date = date if (date and is_valid_date(date)) else get_today_date_str()
    try:
        if ObjectId.is_valid(task_id):
            tasks_collection = get_tasks_collection()
            tasks_collection.delete_one({"_id": ObjectId(task_id)})
    except Exception as e:
        print(f"Error deleting task: {e}")

    return RedirectResponse(f"/?date={target_date}", status_code=303)