from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from db_connection import get_tasks_collection
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    error_message = None
    tasks = []
    total_count = 0
    completed_count = 0
    pending_count = 0
    progress_percentage = 0

    try:
        tasks_collection = get_tasks_collection()
        # Fetch tasks sorted by newest first (descending ObjectId)
        tasks = list(tasks_collection.find().sort("_id", -1))
        
        for task in tasks:
            task["id"] = str(task["_id"])
            if task.get("status") == "Completed":
                completed_count += 1
            else:
                pending_count += 1

        total_count = len(tasks)
        if total_count > 0:
            progress_percentage = round((completed_count / total_count) * 100)
    except Exception as e:
        error_message = (
            "Could not connect to MongoDB. Please ensure your MongoDB Atlas credentials "
            "and network access (0.0.0.0/0 IP whitelist) are configured."
        )
        print(f"Database connection error: {e}")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "tasks": tasks,
            "error": error_message,
            "total_count": total_count,
            "completed_count": completed_count,
            "pending_count": pending_count,
            "progress_percentage": progress_percentage
        }
    )


@app.post("/add")
def add_task(task: str = Form(...), priority: str = Form("Medium")):
    task_text = task.strip()
    if task_text:
        try:
            tasks_collection = get_tasks_collection()
            tasks_collection.insert_one({
                "task_title": task_text,
                "status": "Pending",
                "priority": priority,
                "created_at": datetime.utcnow()
            })
        except Exception as e:
            print(f"Error adding task: {e}")

    return RedirectResponse("/", status_code=303)


@app.get("/toggle/{task_id}")
def toggle_task(task_id: str):
    try:
        tasks_collection = get_tasks_collection()
        task = tasks_collection.find_one({"_id": ObjectId(task_id)})
        if task:
            new_status = "Pending" if task.get("status") == "Completed" else "Completed"
            tasks_collection.update_one(
                {"_id": ObjectId(task_id)},
                {"$set": {"status": new_status}}
            )
    except Exception as e:
        print(f"Error toggling task: {e}")

    return RedirectResponse("/", status_code=303)


@app.get("/complete/{task_id}")
def complete_task(task_id: str):
    try:
        tasks_collection = get_tasks_collection()
        tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"status": "Completed"}}
        )
    except Exception as e:
        print(f"Error completing task: {e}")

    return RedirectResponse("/", status_code=303)


@app.get("/delete/{task_id}")
def delete_task(task_id: str):
    try:
        tasks_collection = get_tasks_collection()
        tasks_collection.delete_one({"_id": ObjectId(task_id)})
    except Exception as e:
        print(f"Error deleting task: {e}")

    return RedirectResponse("/", status_code=303)