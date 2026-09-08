# ✅ TaskMaster - Daily Productivity Dashboard (FastAPI + MongoDB + Google Auth)

A modern, responsive, and secure **Daily Task & Productivity Web Application** built with **FastAPI**, **MongoDB (PyMongo)**, and **Google OAuth2 Authentication**.

---

## 📌 Features

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

---

## 🛠️ Technologies Used

- **Backend**: Python 3.14+, FastAPI, Uvicorn, Starlette
- **Security & Auth**: Google OAuth 2.0 (OpenID Connect), PyJWT, HTTP-only SameSite Cookies
- **Database**: MongoDB Atlas, PyMongo
- **Frontend**: Jinja2 Templates, Vanilla JavaScript, Modern CSS3 Glassmorphism

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd To-Do-List
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Google OAuth & Environment Variables
Create a `.env` file based on `.env.example`:

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

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 📡 API Endpoints

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

---

## 🚢 Deploying to Render / Production

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
