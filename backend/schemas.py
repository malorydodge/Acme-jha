from pydantic import BaseModel
from typing import List, Optional


# -------------------------
# Control
# -------------------------

class ControlBase(BaseModel):
    description: str


class ControlCreate(ControlBase):
    pass


class Control(ControlBase):
    id: int

    class Config:
        orm_mode = True


# -------------------------
# Hazard
# -------------------------

class HazardBase(BaseModel):
    description: str


class HazardCreate(HazardBase):
    controls: List[ControlCreate] = []


class Hazard(HazardBase):
    id: int
    controls: List[Control] = []

    class Config:
        orm_mode = True


# -------------------------
# Step
# -------------------------

class StepBase(BaseModel):
    description: str


class StepCreate(StepBase):
    hazards: List[HazardCreate] = []


class Step(StepBase):
    id: int
    hazards: List[Hazard] = []

    class Config:
        orm_mode = True


# -------------------------
# JHA
# -------------------------

class JHABase(BaseModel):
    title: str
    author: str
    department: Optional[str] = None


class JHACreate(JHABase):
    steps: List[StepCreate] = []


class JHAUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    department: Optional[str] = None


class JHA(JHABase):
    id: int
    steps: List[Step] = []

    class Config:
        orm_mode = True