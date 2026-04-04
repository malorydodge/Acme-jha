from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
import models

router = APIRouter(prefix="/controls", tags=["Controls"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_control(control: dict, db: Session = Depends(get_db)):
    db_control = models.Control(**control)

    db.add(db_control)
    db.commit()
    db.refresh(db_control)

    return db_control