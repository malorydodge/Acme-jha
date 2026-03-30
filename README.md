# Acme-jha

# JHA Web Application

A web-based Job Hazard Analysis (JHA) application for creating, managing, and maintaining workplace safety analyses.

---

# Tech Stack

## Frontend
- Vue 3
- Vite
- Bulma
- Axios

## Backend
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy

---

# Installation

## Backend Setup

```bash
cd backend
python -m venv venv
```

Activate Virtual Environment

Mac/Linux
```
source venv/bin/activate
```
Windows
```
venv\Scripts\activate
```
Install Dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-multipart
```

---

PostgreSQL Setup

Create Database
```bash
CREATE DATABASE jha_app;
```
Update connection string in database.py
```bash
DATABASE_URL = "postgresql://postgres:password@localhost/jha_app"
```

---

Run Backend
```bash
uvicorn main:app --reload
```
Backend URL
```
http://localhost:8000
```
API Documentation
```
http://localhost:8000/docs
```

---

Frontend Setup
```bash
cd frontend
npm install
```
Run Frontend
```bash
npm run dev
```
Frontend URL
```
http://localhost:5173
```

---

Author

Malory Dodge


---

License

This project is for assessment purposes only.

.
