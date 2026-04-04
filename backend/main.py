from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routes import jhas, steps, hazards, controls


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jhas.router)
app.include_router(steps.router)
app.include_router(hazards.router)
app.include_router(controls.router)

origins = [
    "http://localhost:8080", 
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # Allows specific origins
    allow_credentials=True,        # Allows cookies/auth headers to be sent
    allow_methods=["*"],           # Allows all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],           # Allows all headers (Content-Type, Authorization, etc.)
)
