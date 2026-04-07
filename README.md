# Acme JHA

A web-based Job Hazard Analysis (JHA) application for creating, managing, and maintaining workplace safety analyses.

This application allows users to create structured Job Hazard Analyses with steps, hazards, controls, and supporting documentation including images.

---

# Live Demo

Frontend:
Backend API: https://acme-jha-production.up.railway.app/

---

# Features

- Create, edit, and delete JHAs
- Add steps to each JHA
- Add hazards to each step
- Add controls to each hazard
- Upload step images
- Drag-and-drop step reordering
- Expandable/collapsible step views
- Form validation
- Responsive UI

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

# Local Installation

# Backend Setup

Clone Repository

```
git clone https://github.com/malorydodge/Acme-jha.git
cd Acme-jha
```

Create Virtual Environment

```
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

```
pip install -r requirements.txt
```

---

# PostgreSQL Setup

Install PostgreSQL if not already installed

Create Database

```
CREATE DATABASE jha_app;
```

Update connection string in database.py

```
DATABASE_URL = "postgresql://postgres:password@localhost/jha_app"
```

---

# File Upload Setup

Create uploads directory

```
mkdir uploads
```

---

# Run Backend

```
uvicorn main:app --reload
```

Backend URL

```
http://localhost:8000
```

API Docs

```
http://localhost:8000/docs
```

---

# Frontend Setup

```
cd frontend
npm install
```

Run Frontend

```
npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# Deployment

This project is deployed using:

Frontend: Vercel
Backend: Railway
Database: Railway PostgreSQL

---

# Environment Variables

Backend (.env)

```
DATABASE_URL=
```

Frontend (.env)

```
VITE_API_URL=
```

---

# Author

Malory Dodge

---

# License

This project is for assessment purposes only.
