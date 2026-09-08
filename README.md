# ✅ TaskMaster - Daily Productivity Dashboard & To-Do List

A modern, full-featured **Daily Productivity & Task Management Web Application** built with **FastAPI**, **MongoDB Atlas (PyMongo)**, and a custom **Glassmorphic Vanilla CSS Design System** featuring daily task isolation, Pomodoro focus timer, streak tracking, and 7-day activity heatmaps.

---

## ✨ Key Features

### 📅 Daily Task Isolation & Navigation
- **Per-Date Task Storage**: Each day's tasks are tracked and persisted independently (`YYYY-MM-DD`).
- **Interactive Date Switcher**: Quickly switch between days with **Prev**, **Today**, **Next** buttons, or pick any specific day using the integrated calendar date picker.

### 💾 Batch Persistence & Unsaved Changes Guard
- **One-Click Save & Keyboard Shortcut**: Save all changes for the day with one click or press `Ctrl + S` (`Cmd + S` on macOS).
- **Unsaved Changes Tracking**: Visual live dirty-state indicator and interactive switch prompt to prevent accidental data loss when navigating between dates.

### 🔥 Daily Streaks & 7-Day Activity Heatmap
- **Streak Counter**: Automatically calculates consecutive days with completed tasks.
- **7-Day Mini Heatmap Strip**: Visual weekly overview displaying daily completion progress chips with direct date navigation.

### ⏱️ Integrated Pomodoro Focus Timer
- **Preset & Custom Durations**: Choose from Focus (25m), Short Break (5m), Long Break (15m), or configure Custom hour/minute intervals.
- **Active Task Linking**: Select and attach any pending task directly to your focus session.
- **Circular Progress Ring & Web Audio Chime**: Animated progress countdown with synthesized audio alarm bell and visual completion pulse.

### 🎨 Themes & Custom Accent Palettes
- **Dark / Light Mode**: Smooth theme toggle with persistent `localStorage` preference.
- **6 Vibrant Accent Colors**: Electric Blue, Amethyst Purple, Neon Emerald, Rose Pink, Sunset Amber, and Cyber Cyan.

### 📋 Rich Task Management & Organization
- **6 Categories**: Work 💼, Personal 👤, Study 📚, Health 🏋️, Finance 💰, and General 🏷️.
- **3 Priority Levels**: High 🔴, Medium 🟡, and Low 🟢 with distinct visual badges.
- **Expandable Notes / Subtasks**: Add multi-line notes, links, and subtasks with expandable accordion drawers.
- **Drag & Drop Reordering**: Reorder tasks intuitively with smooth drag-and-drop handles.
- **Square Checkbox Toggles**: Modern square toggle buttons for marking tasks pending/completed.

### 🔍 Live Search, Filters & Statistics
- **Status Tabs**: Instant tab filters for All, Pending, and Completed tasks.
- **Category Filter Dropdown & Search Bar**: Filter by category or search task titles and notes in real time.
- **Productivity Dashboard Counters**: Live metrics for Total Tasks, Pending, Completed, and Completion Rate %.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Database** | [MongoDB Atlas](https://www.mongodb.com/atlas) (via [PyMongo](https://pymongo.readthedocs.io/)) |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) |
| **Frontend Styling** | Vanilla CSS3 (Custom Glassmorphism, Aurora Blobs, Inter Font & Font Awesome 6) |
| **Audio Engine** | Web Audio API (Synthesized Bell Chime) |
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
*(Or `python -m uvicorn main:app --reload`)*

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :--- | :--- |
| `Enter` (in task input) | Add new task |
| `Ctrl + S` / `Cmd + S` | Save current day's tasks to database |
| `Escape` | Close any open modal / prompt |

---

## 📡 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Server-rendered HTML dashboard (`?date=YYYY-MM-DD`). |
| `GET` | `/api/tasks` | Fetch tasks and completion stats for a specific date (`?date=YYYY-MM-DD`). |
| `GET` | `/api/stats/streak` | Fetch daily streak count and 7-day activity heatmap data. |
| `POST` | `/api/tasks/save` | Bulk save all tasks for a specific date (preserves ordering, categories, notes). |
| `POST` | `/api/tasks` | Create a single task for a date. |
| `PUT` | `/api/tasks/{task_id}` | Update task title, priority, category, notes, or status. |
| `POST` | `/api/tasks/{task_id}/toggle` | Toggle task completion status between Pending and Completed. |
| `DELETE` | `/api/tasks/{task_id}` | Delete a task by ID. |

---

## 🚢 Deploying to Render

1. Push your code to your GitHub repository:
   ```bash
   git add .
   git commit -m "Update project documentation and features"
   git push origin main
   ```
2. In your **[Render Dashboard](https://dashboard.render.com/)**:
   - Create a new **Web Service** connected to your repository.
   - Configure the service settings:
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Under **Environment Variables**:
     - `MONGO_URI`: Your MongoDB Atlas connection URI.
     - `MONGO_DB_NAME`: Database name (e.g., `todo_app`).
3. Click **Deploy Web Service**.
