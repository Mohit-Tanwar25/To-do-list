# ✅ TaskMaster - Daily To-Do List Application (FastAPI + MongoDB)

A modern, responsive **Daily To-Do List Web Application** built with **FastAPI** and **MongoDB (PyMongo)** with per-day task isolation and persistent saving.

---

## ✨ Features

- 📅 **Daily Task Isolation**: Each day's tasks are stored and managed separately (`YYYY-MM-DD`).
- 💾 **Dedicated Save Button**: Save all tasks for the selected date with one click; unsaved changes indicator prevents accidental data loss.
- 📆 **Interactive Date Navigation**: Fast date switcher (Prev / Today / Next) and calendar date picker.
- ✏️ **Full Task Management**: Add, inline edit, toggle completion, and delete tasks.
- 🏷️ **Priority Badges**: Organize tasks by priority level (High, Medium, Low).
- 📊 **Real-Time Productivity Statistics**: Dynamic counters for total, pending, completed tasks, and completion rate.
- 🔍 **Live Search & Filter Tabs**: Filter by All, Pending, Completed, or search by keyword in real time.
- ☁️ **Cloud Database Persistence**: Backed by MongoDB Atlas with connection pooling and retry capabilities.
- 🚀 **Render Ready**: Optimized for direct deployment on Render.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Database** | [MongoDB Atlas](https://www.mongodb.com/atlas) (via [PyMongo](https://pymongo.readthedocs.io/)) |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) |
| **Styling** | Vanilla CSS3 (Custom Design System with Inter typography & Font Awesome 6) |
| **Environment Config** | [python-dotenv](https://github.com/theskumar/python-dotenv) |

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Mohit-Tanwar25/To-do-list.git
cd To-do-list
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory (or copy from `.env.example`):
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=todo_app
```

### 4. Start the Application Server
```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📡 API Endpoints

- `GET /`: Server-side rendered dashboard (accepts optional `?date=YYYY-MM-DD`).
- `GET /api/tasks?date=YYYY-MM-DD`: Fetch tasks and statistics for a specific date.
- `POST /api/tasks/save`: Bulk save all tasks for a specific date.
- `POST /api/tasks`: Create a single task for a date.
- `PUT /api/tasks/{task_id}`: Update task title, priority, or completion status.
- `POST /api/tasks/{task_id}/toggle`: Toggle task completion status.
- `DELETE /api/tasks/{task_id}`: Delete task by ID.

---

## 🚢 Deploying to Render

1. Push your changes to your GitHub repository:
   ```bash
   git add .
   git commit -m "Add daily task saving and date navigation"
   git push origin main
   ```
2. In your **Render Dashboard**:
   - Go to your Web Service.
   - Under **Settings**:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Under **Environment Variables**:
     - Ensure `MONGO_URI` is set to your MongoDB Atlas connection string.
     - Ensure `MONGO_DB_NAME` is set (defaults to `todo_app`).
3. Click **Manual Deploy** -> **Deploy latest commit** (or auto-deploy on push).
