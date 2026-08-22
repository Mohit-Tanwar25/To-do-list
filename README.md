# ✅ To-Do List Application (FastAPI + MongoDB)

A modern, responsive **To-Do List Web Application** built with **FastAPI** and **MongoDB (PyMongo)**.

---

## 📌 Features

- ✅ Add new tasks with priority levels (High, Medium, Low)
- ✅ Mark tasks as completed
- ✅ Delete tasks
- ✅ Real-time persistence using MongoDB Atlas / Local MongoDB
- ✅ Server-side rendering using Jinja2 Templates & CSS styling

---

## 🛠️ Technologies Used

- **Python 3**
- **FastAPI**
- **Uvicorn**
- **MongoDB & PyMongo**
- **Jinja2 Templates**
- **HTML5 & CSS3**

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

### 3. Setup environment variables
Create a `.env` file from `.env.example`:
```env
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=todo_app
```

### 4. Run the application
```bash
uvicorn main:app --reload
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
