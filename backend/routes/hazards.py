from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
import models

router = APIRouter(prefix="/hazard", tags=["Hazard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_hazard(hazard: dict, db: Session = Depends(get_db)):
    db_hazard = models.Hazard(**hazard)

    db.add(db_hazard)
    db.commit()
    db.refresh(db_hazard)

    return db_hazard