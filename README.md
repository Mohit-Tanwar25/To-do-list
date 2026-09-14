# ✅ TaskMaster — Daily Productivity Dashboard

A modern, responsive, and secure **Daily Task & Productivity Web Application** built with **FastAPI**, **MongoDB Atlas**, and **Google OAuth 2.0**.

TaskMaster helps users organize daily tasks, track productivity, maintain completion streaks, and stay focused with an integrated **Pomodoro timer** — all through a clean, modern glassmorphism interface.

---

## ✨ Features

### 🔐 Authentication & Security

* **Google OAuth 2.0 Authentication** for secure account access.
* Persistent **HTTP-only session cookies**.
* Automatic user profile provisioning.
* Secure logout functionality.
* Strict **multi-user data isolation**.
* Users can access and modify only their own tasks.

### 📅 Daily Task Management

* Organize tasks independently for each date.
* Tasks are stored using the `YYYY-MM-DD` format.
* Navigate between dates using:

  * Previous Day
  * Today
  * Next Day
  * Calendar Date Picker
* Add, edit, delete, reorder, and complete tasks.
* Bulk save support for efficient updates.
* Unsaved changes indicator to prevent accidental data loss.

### 🏷️ Categories & Priorities

Organize tasks using six categories:

* 💼 Work
* 👤 Personal
* 📚 Study
* 🏋️ Health
* 💰 Finance
* 🏷️ General

Set task priorities using:

* 🔴 High
* 🟡 Medium
* 🟢 Low

Tasks can also include:

* Multi-line notes
* Links
* Subtasks
* Completion status

### 🔍 Search, Filters & Statistics

* Real-time task search.
* Filter tasks by category.
* Filter by:

  * All
  * Pending
  * Completed
* Live productivity statistics:

  * Total Tasks
  * Pending Tasks
  * Completed Tasks
  * Completion Rate

### 🔥 Productivity Streaks

* Automatically tracks consecutive productive days.
* Displays the current completion streak.
* Includes a **7-day activity heatmap**.
* Quickly navigate to a specific day from the activity overview.

### ⏱️ Pomodoro Focus Timer

Stay focused with an integrated Pomodoro timer.

Available presets:

* 🎯 Focus — 25 minutes
* ☕ Short Break — 5 minutes
* 🌙 Long Break — 15 minutes
* ⚙️ Custom Duration

Additional functionality includes:

* Link a timer session to a specific task.
* Circular progress indicator.
* Visual completion feedback.
* Web Audio API notification chime.

### 🎨 Themes & Customization

* 🌙 Dark Mode
* ☀️ Light Mode
* Persistent theme preferences using `localStorage`.
* Six customizable accent palettes:

  * Electric Blue
  * Amethyst Purple
  * Neon Emerald
  * Rose Pink
  * Sunset Amber
  * Cyber Cyan

---

## 🛠️ Tech Stack

| Layer                      | Technology                        |
| :------------------------- | :-------------------------------- |
| **Language**               | Python 3.14+                      |
| **Backend Framework**      | FastAPI                           |
| **Application Server**     | Uvicorn                           |
| **Database**               | MongoDB Atlas                     |
| **Database Driver**        | PyMongo                           |
| **Authentication**         | Google OAuth 2.0 / OpenID Connect |
| **Session Security**       | HTTP-only SameSite Cookies        |
| **Token Handling**         | PyJWT                             |
| **Frontend**               | HTML5, Vanilla JavaScript         |
| **Styling**                | Modern CSS3 / Glassmorphism       |
| **Templating**             | Jinja2                            |
| **Audio**                  | Web Audio API                     |
| **Environment Management** | python-dotenv                     |

---

## 📂 Project Structure

```text
To-do-list/
│
├── main.py                  # FastAPI application
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variable template
├── .gitignore
├── README.md
│
├── templates/
│   └── ...                  # Jinja2 HTML templates
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...                  # Frontend assets
│
└── ...
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Mohit-Tanwar25/To-do-list.git
cd To-do-list
```

### 2. Install Dependencies

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Configuration

Create a `.env` file in the project root based on `.env.example`.

```env
# MongoDB Atlas
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=todo_app

# Application Security
SECRET_KEY=your-super-secret-jwt-key

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Optional
# GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
```

> ⚠️ **Important:** Never commit your `.env` file, MongoDB credentials, OAuth secrets, or other sensitive credentials to GitHub.

---

## 🔐 Setting Up Google OAuth

To enable Google authentication:

1. Open **Google Cloud Console**.
2. Navigate to **APIs & Services → Credentials**.
3. Select **Create Credentials → OAuth 2.0 Client ID**.
4. Choose **Web application** as the application type.
5. Add the following authorized redirect URIs.

### Local Development

```text
http://localhost:8000/auth/google/callback
http://127.0.0.1:8000/auth/google/callback
```

### Production

```text
https://<your-app-domain>/auth/google/callback
```

6. Copy the generated **Client ID** and **Client Secret** into your `.env` file.

---

## ▶️ Run the Application

Start the FastAPI development server:

```bash
uvicorn main:app --reload
```

Or:

```bash
python -m uvicorn main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

Open the URL in your browser and sign in using Google.

---

## ⌨️ Keyboard Shortcuts

| Shortcut   | Action                        |
| :--------- | :---------------------------- |
| `Enter`    | Add a new task                |
| `Ctrl + S` | Save the current day's tasks  |
| `Cmd + S`  | Save tasks on macOS           |
| `Escape`   | Close an open modal or prompt |

---

## 📡 API Reference

### 🔐 Authentication & Pages

| Method | Endpoint                | Description                                   |
| :----- | :---------------------- | :-------------------------------------------- |
| `GET`  | `/`                     | Main productivity dashboard                   |
| `GET`  | `/login`                | Google login page                             |
| `GET`  | `/auth/google`          | Initiates Google OAuth authentication         |
| `GET`  | `/auth/google/callback` | Handles Google OAuth callback                 |
| `GET`  | `/auth/logout`          | Clears the user's session                     |
| `GET`  | `/auth/dev-login`       | Development helper for testing user isolation |

### 📋 Task Management

| Method   | Endpoint                      | Description                          |
| :------- | :---------------------------- | :----------------------------------- |
| `GET`    | `/api/tasks?date=YYYY-MM-DD`  | Fetch tasks for a specific date      |
| `GET`    | `/api/stats/streak`           | Fetch streak and 7-day activity data |
| `POST`   | `/api/tasks`                  | Create a new task                    |
| `POST`   | `/api/tasks/save`             | Bulk save tasks for a specific date  |
| `PUT`    | `/api/tasks/{task_id}`        | Update an existing task              |
| `POST`   | `/api/tasks/{task_id}/toggle` | Toggle task completion               |
| `DELETE` | `/api/tasks/{task_id}`        | Delete a task                        |

All task-related endpoints are protected and operate within the authenticated user's account.

---

## ☁️ Database

TaskMaster uses **MongoDB Atlas** for cloud-based data persistence.

The application stores task information according to:

```text
User
 └── Date
      └── Tasks
           ├── Title
           ├── Category
           ├── Priority
           ├── Notes
           ├── Subtasks
           ├── Status
           └── Order
```

Tasks are associated with both the authenticated user and their selected date, ensuring that users can maintain separate daily task lists while keeping accounts isolated from one another.

---

## 🚢 Deployment

TaskMaster can be deployed to platforms such as:

* Render
* Railway
* AWS
* Other platforms supporting Python/FastAPI applications

### Production Environment Variables

Configure the following variables in your hosting provider:

```env
MONGO_URI=your-mongodb-connection-string
MONGO_DB_NAME=todo_app
SECRET_KEY=your-strong-secret-key
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

### Production Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

For production deployment, make sure your application's production callback URL is also configured in Google Cloud Console.

Example:

```text
https://your-app.onrender.com/auth/google/callback
```

---

## 🔒 Security Considerations

TaskMaster is designed with user privacy and secure authentication in mind.

Key security practices include:

* Google OAuth 2.0 authentication.
* HTTP-only session cookies.
* SameSite cookie protection.
* User-level task ownership validation.
* Database-level user isolation.
* Environment variables for sensitive credentials.
* No hardcoded production secrets.

---

## 🎯 Future Improvements

Potential improvements for future versions include:

* 📱 Progressive Web App (PWA) support
* 🔔 Task reminders and notifications
* 📊 Advanced productivity analytics
* 📅 Calendar integration
* 🔄 Recurring tasks
* 📤 Task export/import
* 🏆 Productivity achievements
* 👥 Collaborative task lists
* 🤖 AI-powered task suggestions

---

## 📸 Project Highlights

TaskMaster combines productivity tools into a single dashboard:

```text
┌─────────────────────────────────────────────┐
│              TASKMASTER                     │
│        Daily Productivity Dashboard         │
├─────────────────────────────────────────────┤
│                                             │
│  📅 Daily Tasks        🔥 Streak            │
│                                             │
│  ☑ Complete tasks     📊 Statistics         │
│                                             │
│  ⏱ Pomodoro Timer     🎨 Themes             │
│                                             │
│  🔍 Search & Filter   📈 Activity Heatmap    │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 👨‍💻 Author

**Mohit Tanwar**

BCA student and aspiring software developer passionate about technology, programming, and building innovative, scalable solutions that turn ideas into real-world impact.

---


**Built with ❤️ using FastAPI, MongoDB, JavaScript, and modern web technologies.**
