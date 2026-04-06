from pydantic import BaseModel
from typing import List, Optional


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
    photo: Optional[str]  # NEW
    hazards: List[Hazard] = []

    class Config:
        from_attributes = True


class JHABase(BaseModel):
    title: str
    author: str
    department: str


class JHACreate(JHABase):
    steps: List[Step] = []


class JHA(JHABase):
    id: int
    steps: List[Step] = []

    class Config:
        from_attributes = True