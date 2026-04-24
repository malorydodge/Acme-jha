from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Control(BaseModel):
    id: Optional[int]
    description: str

    class Config:
        from_attributes = True


class Hazard(BaseModel):
    id: Optional[int]
    description: str
    consequence: Optional[str]
    controls: List[Control] = []

    class Config:
        from_attributes = True


class Step(BaseModel):
    id: Optional[int]
    description: str
    notes: Optional[str] = None
    completed: bool = False
    photo: Optional[str]
    hazards: List[Hazard] = []

    class Config:
        from_attributes = True


class JHABase(BaseModel):
    title: str
    author: str
    department: str
    location: Optional[str] = None
    job_title: Optional[str] = None
    supervisor: Optional[str] = None
    job_date: Optional[date] = Field(default=None)


class JHACreate(JHABase):
    steps: List[Step] = []


class JHA(JHABase):
    id: int
    steps: List[Step] = []

    class Config:
        from_attributes = True