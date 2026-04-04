from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
import models

router = APIRouter(prefix="/steps", tags=["Steps"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_step(step: dict, db: Session = Depends(get_db)):
    db_step = models.Step(**step)

    db.add(db_step)
    db.commit()
    db.refresh(db_step)

    return db_step