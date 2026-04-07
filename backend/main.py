from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import jhas, steps, hazards, controls
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

models.Base.metadata.create_all(bind=engine)

app.include_router(jhas.router)
app.include_router(steps.router)
app.include_router(hazards.router)
app.include_router(controls.router)

# origins = [
#     "http://localhost:8080", 
#     "http://localhost:5173",
#     "https://acme-ayoyrtlrr-malory-dodges-projects.vercel.app/",
#     "https://acme-jha-production.up.railway.app/",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allows specific origins
    allow_credentials=True,        # Allows cookies/auth headers to be sent
    allow_methods=["*"],           # Allows all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],           # Allows all headers (Content-Type, Authorization, etc.)
)
