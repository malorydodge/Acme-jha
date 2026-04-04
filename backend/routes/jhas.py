from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from database import SessionLocal
import models
import schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/jhas")
def get_jhas(db: Session = Depends(get_db)):
    return db.query(models.JHA).all()

@router.post("/jhas")
def create_jha(jha: schemas.JHACreate, db: Session = Depends(get_db)):
    db_jha = models.JHA(
        title=jha.title,
        author=jha.author,
        department=jha.department
    )

    db.add(db_jha)
    db.commit()
    db.refresh(db_jha)

    return db_jha

@router.get("/jhas/{jha_id}")
def get_jha(jha_id: int, db: Session = Depends(get_db)):
    jha = db.query(models.JHA).filter(models.JHA.id == jha_id).first()
    if not jha:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="JHA not found")
    return jha

@router.put("/jhas/{jha_id}")
def update_jha(jha_id: int, updated_data: schemas.JHAUpdate, db: Session = Depends(get_db)):
    db_jha = db.query(models.JHA).filter(models.JHA.id == jha_id).first()
    
    if not db_jha:
        raise HTTPException(status_code=404, detail="JHA not found")

    update_dict = updated_data.dict(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_jha, key, value)

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