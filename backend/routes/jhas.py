from fastapi import APIRouter, Depends, Response, Form, status, HTTPException, UploadFile, File
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
import json
import os
import shutil
import uuid

from database import SessionLocal
import models
import schemas

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_upload(file: UploadFile):
    if not file:
        return None

    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/jhas", response_model=list[schemas.JHA])
def get_jhas(db: Session = Depends(get_db)):
    return db.query(models.JHA).all()


@router.post("/jhas", response_model=schemas.JHA)
async def create_jha(
    title: str = Form(...),
    author: str = Form(...),
    department: str = Form(...),
    steps: Optional[str] = Form(None),
    photos: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    steps_data = json.loads(steps) if steps else []

    jha = models.JHA(
        title=title,
        author=author,
        department=department
    )

    db.add(jha)
    db.commit()
    db.refresh(jha)

    photo_index = 0

    for step_data in steps_data:
        photo_path = None

        if photo_index < len(photos):
            photo_path = save_upload(photos[photo_index])
            photo_index += 1

        step = models.Step(
            description=step_data["description"],
            photo=photo_path,
            jha_id=jha.id
        )

        db.add(step)
        db.commit()
        db.refresh(step)

        for hazard_data in step_data.get("hazards", []):
            hazard = models.Hazard(
                description=hazard_data["description"],
                consequence=hazard_data.get("consequence"),
                step_id=step.id
            )

            db.add(hazard)
            db.commit()
            db.refresh(hazard)

            for control_data in hazard_data.get("controls", []):
                control = models.Control(
                    description=control_data["description"],
                    hazard_id=hazard.id
                )

                db.add(control)

    db.commit()
    return jha


@router.get("/jhas/{jha_id}", response_model=schemas.JHA)
def get_jha(jha_id: int, db: Session = Depends(get_db)):
    jha = (
        db.query(models.JHA)
        .options(
            joinedload(models.JHA.steps)
            .joinedload(models.Step.hazards)
            .joinedload(models.Hazard.controls)
        )
        .filter(models.JHA.id == jha_id)
        .first()
    )

    if not jha:
        raise HTTPException(status_code=404, detail="JHA not found")

    return jha


@router.put("/jhas/{jha_id}", response_model=schemas.JHA)
async def update_jha(
    jha_id: int,
    title: str = Form(...),
    author: str = Form(...),
    department: str = Form(...),
    steps: Optional[str] = Form(None),
    photos: List[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    db_jha = (
        db.query(models.JHA)
        .options(
            joinedload(models.JHA.steps)
            .joinedload(models.Step.hazards)
            .joinedload(models.Hazard.controls)
        )
        .filter(models.JHA.id == jha_id)
        .first()
    )

    if not db_jha:
        raise HTTPException(status_code=404, detail="JHA not found")

    steps_data = json.loads(steps) if steps else []

    db_jha.title = title
    db_jha.author = author
    db_jha.department = department

    db_jha.steps.clear()

    photo_index = 0

    for step_data in steps_data:
        photo_path = None

        if photo_index < len(photos):
            photo_path = save_upload(photos[photo_index])
            photo_index += 1

        db_step = models.Step(
            description=step_data["description"],
            photo=photo_path
        )

        for hazard_data in step_data.get("hazards", []):
            db_hazard = models.Hazard(
                description=hazard_data["description"],
                consequence=hazard_data.get("consequence")
            )

            for control_data in hazard_data.get("controls", []):
                db_control = models.Control(
                    description=control_data["description"]
                )

                db_hazard.controls.append(db_control)

            db_step.hazards.append(db_hazard)

        db_jha.steps.append(db_step)

    db.commit()
    db.refresh(db_jha)

    return db_jha


@router.delete("/jhas/{jha_id}")
def delete_jha(jha_id: int, db: Session = Depends(get_db)):
    db_jha = db.query(models.JHA).filter(models.JHA.id == jha_id).first()

    if not db_jha:
        raise HTTPException(status_code=404, detail="JHA not found")

    db.delete(db_jha)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)