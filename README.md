# ⚡ TaskMaster — Modern Minimalist To-Do App

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

A clean, modern, and minimal **productivity & task management dashboard** built with **FastAPI**, **Jinja2**, and **MongoDB Atlas**. Designed with a distraction-free SaaS user interface, real-time metrics, live search, and smooth modal confirmations.

---

## ✨ Features

- 🎯 **Minimal SaaS Dashboard**: Clean, distraction-free productivity layout inspired by modern web apps.
- 📊 **Real-time Analytics**: Live statistics cards tracking Total Tasks, Pending Tasks, Completed Tasks, and Progress Completion Rate.
- ⚡ **Real-time Search & Filtering**: Instant client-side search and category filtering (**All**, **Pending**, **Completed**) with zero page reloads.
- 🏷️ **Priority Tagging**: Organize tasks by priority levels (🔴 High, 🟡 Medium, 🟢 Low) with tailored color badges.
- 🛡️ **Modern Confirmation Modal**: Custom non-intrusive modal dialog for task deletions, replacing native browser alerts.
- ☁️ **Cloud Database**: Persistent cloud storage powered by **MongoDB Atlas** with PyMongo.
- 📱 **Fully Responsive**: Fluid desktop, tablet, and mobile interface with clean touch targets.
- 🎨 **Custom Favicon**: Distinctive vector SVG browser tab icon.

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

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

Interactive API Swagger documentation is available at:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📁 Project Structure

```
├── main.py              # FastAPI application routes & endpoints
├── db_connection.py     # MongoDB Atlas client connection logic
├── requirements.txt     # Python dependencies
├── .env.example         # Template for environment variables
├── .gitignore           # Git ignore rules (protects credentials)
├── static/
│   ├── favicon.svg      # Custom SVG tab icon
│   └── style.css        # Dashboard styling & responsive layout
└── templates/
    └── index.html       # Jinja2 dashboard template with embedded styles & modals
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
