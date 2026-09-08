<<<<<<< HEAD
# ✅ TaskMaster - Daily Productivity Dashboard & To-Do List

A modern, full-featured **Daily Productivity & Task Management Web Application** built with **FastAPI**, **MongoDB Atlas (PyMongo)**, and a custom **Glassmorphic Vanilla CSS Design System** featuring daily task isolation, Pomodoro focus timer, streak tracking, and 7-day activity heatmaps.
=======
# ✅ TaskMaster - Daily Productivity Dashboard (FastAPI + MongoDB + Google Auth)

A modern, responsive, and secure **Daily Task & Productivity Web Application** built with **FastAPI**, **MongoDB (PyMongo)**, and **Google OAuth2 Authentication**.
>>>>>>> mohit/main

---

## ✨ Key Features

<<<<<<< HEAD
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
=======
- 🔐 **Google OAuth2 Authentication**: Secure sign-in with Google accounts, persistent HTTP-only sessions, and auto-provisioning of user profiles.
- 🔒 **Strict Multi-Tenant Task Privacy**: Complete database-level user isolation—tasks created by User A are strictly invisible and inaccessible to User B.
- 📅 **Daily Task Planner**: Tasks are organized and saved per date (`YYYY-MM-DD`).
- 💾 **Bulk & Single Save Operations**: Dedicated save and autosave actions with visual change indicators.
- 📆 **Interactive Date Navigation**: Fast date switcher (Prev / Today / Next) and calendar date picker.
- ✏️ **Full Task Management**: Add, inline edit, reorder, categorize, prioritize, and delete tasks.
- 🏷️ **Categories & Priority Badges**: Work, Personal, Study, Health, Finance, and General with High / Medium / Low urgency tags.
- 🔥 **Streak Tracker & 7-Day Heatmap**: Visual streak calculation and 7-day completion activity per user.
- ⏱️ **Focus Pomodoro Timer**: Integrated customizable timer with focus, short break, and long break intervals.
- 🎨 **Theme & Accent Customization**: Light/Dark modes with dynamic theme palettes (Blue, Purple, Emerald, Rose, Amber, Cyan).
- 👤 **Google User Profile Badge**: Shows avatar, display name, email, and one-click secure Sign Out.
- ☁️ **Cloud Database Persistence**: Backed by MongoDB Atlas with connection pooling and retry capabilities.
- 🚀 **Production Ready**: Optimized for deployment on Render, Railway, or AWS.
>>>>>>> mohit/main

---

## 🛠️ Tech Stack

<<<<<<< HEAD
| Layer | Technology |
| :--- | :--- |
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **Server** | [Uvicorn](https://www.uvicorn.org/) |
| **Database** | [MongoDB Atlas](https://www.mongodb.com/atlas) (via [PyMongo](https://pymongo.readthedocs.io/)) |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) |
| **Frontend Styling** | Vanilla CSS3 (Custom Glassmorphism, Aurora Blobs, Inter Font & Font Awesome 6) |
| **Audio Engine** | Web Audio API (Synthesized Bell Chime) |
| **Environment Config** | [python-dotenv](https://github.com/theskumar/python-dotenv) |
=======
- **Backend**: Python 3.14+, FastAPI, Uvicorn, Starlette
- **Security & Auth**: Google OAuth 2.0 (OpenID Connect), PyJWT, HTTP-only SameSite Cookies
- **Database**: MongoDB Atlas, PyMongo
- **Frontend**: Jinja2 Templates, Vanilla JavaScript, Modern CSS3 Glassmorphism
>>>>>>> mohit/main

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

<<<<<<< HEAD
### 3. Configure Environment Variables
Create a `.env` file in the root directory (or copy from `.env.example`):
=======
### 3. Configure Google OAuth & Environment Variables
Create a `.env` file based on `.env.example`:

>>>>>>> mohit/main
```env
# MongoDB Atlas Connection
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=todo_app

# Application Security Key
SECRET_KEY=your-super-secret-jwt-key

# Google OAuth Credentials
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional: Override redirect URI (Defaults automatically to {base_url}/auth/google/callback)
# GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

#### Setting up Google Cloud OAuth:
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Navigate to **APIs & Services > Credentials**.
3. Click **Create Credentials > OAuth 2.0 Client IDs** (Application Type: **Web application**).
4. Add **Authorized redirect URIs**:
   - For local development: `http://localhost:8000/auth/google/callback` and `http://127.0.0.1:8000/auth/google/callback`
   - For production: `https://<your-app-domain>/auth/google/callback`
5. Copy your **Client ID** and **Client Secret** into your `.env` file.

### 4. Run the application
```bash
uvicorn main:app --reload
```
*(Or `python -m uvicorn main:app --reload`)*

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## ⌨️ Keyboard Shortcuts

<<<<<<< HEAD
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
=======
### Authentication & Pages
- `GET /`: Main dashboard (redirects to `/login` if unauthenticated).
- `GET /login`: Login page with "Continue with Google" button.
- `GET /auth/google`: Initiates Google OAuth2 consent screen.
- `GET /auth/google/callback`: Handles Google OAuth callback, verifies state, upserts user, and issues session cookie.
- `GET /auth/logout`: Clears session token and signs out.
- `GET /auth/dev-login`: Development helper to quickly test multi-account isolation (`?account=user_a` vs `?account=user_b`).

### Task Management (Protected - User Isolated)
- `GET /api/tasks?date=YYYY-MM-DD`: Fetch tasks and statistics for the authenticated user on a date.
- `GET /api/stats/streak`: Fetch the authenticated user's streak and 7-day activity heatmap.
- `POST /api/tasks/save`: Bulk save all tasks for a date (scoped strictly to the user).
- `POST /api/tasks`: Create a single task for the authenticated user.
- `PUT /api/tasks/{task_id}`: Update task details (verifies user ownership).
- `POST /api/tasks/{task_id}/toggle`: Toggle task completion (verifies user ownership).
- `DELETE /api/tasks/{task_id}`: Delete task (verifies user ownership).
>>>>>>> mohit/main

---

## 🚢 Deploying to Render / Production

<<<<<<< HEAD
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
=======
1. Set your environment variables in your hosting provider's dashboard:
   - `MONGO_URI`: Your MongoDB connection string.
   - `MONGO_DB_NAME`: `todo_app`
   - `SECRET_KEY`: A strong random string.
   - `GOOGLE_CLIENT_ID`: Your Google OAuth Client ID.
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth Client Secret.
2. Ensure your production domain callback URL (e.g. `https://<your-app>.onrender.com/auth/google/callback`) is added to **Authorized Redirect URIs** in Google Cloud Console.
3. Start command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
>>>>>>> mohit/main
