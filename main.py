from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bson import ObjectId
from db_connection import get_tasks_collection

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    error_message = None
    tasks = []
    try:
        tasks_collection = get_tasks_collection()
        tasks = list(tasks_collection.find())
        for task in tasks:
            task["id"] = str(task["_id"])
    except Exception as e:
        error_message = (
            "Could not connect to MongoDB. Please ensure your MongoDB Atlas credentials "
            "and network access (0.0.0.0/0 IP whitelist) are configured."
        )
        print(f"Database connection error: {e}")

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tasks": tasks, "error": error_message}
    )


@app.post("/add")
def add_task(task: str = Form(...), priority: str = Form(...)):
    try:
        tasks_collection = get_tasks_collection()
        tasks_collection.insert_one({
            "task_title": task,
            "status": "Pending",
            "priority": priority
        })
    except Exception as e:
        print(f"Error adding task: {e}")

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