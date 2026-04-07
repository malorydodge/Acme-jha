from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import jhas, steps, hazards, controls
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

origins = [
    "http://localhost:8080", 
    "http://localhost:5173",
    "https://acme-jha-production.up.railway.app",
    "https://acme-jha.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

models.Base.metadata.create_all(bind=engine)

app.include_router(jhas.router)
app.include_router(steps.router)
app.include_router(hazards.router)
app.include_router(controls.router)

