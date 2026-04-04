from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


class JHA(Base):
    __tablename__ = "jhas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    department = Column(String)

    steps = relationship("Step", back_populates="jha", cascade="all, delete")

class Step(Base):
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    jha_id = Column(Integer, ForeignKey("jhas.id"))

    jha = relationship("JHA", back_populates="steps")
    hazards = relationship("Hazard", back_populates="step", cascade="all, delete")

class Hazard(Base):
    __tablename__ = "hazards"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    consequence = Column(Text)
    step_id = Column(Integer, ForeignKey("steps.id"))

    step = relationship("Step", back_populates="hazards")
    controls = relationship("Control", back_populates="hazard", cascade="all, delete")


class Control(Base):
    __tablename__ = "controls"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    hazard_id = Column(Integer, ForeignKey("hazards.id"))

    hazard = relationship("Hazard", back_populates="controls")