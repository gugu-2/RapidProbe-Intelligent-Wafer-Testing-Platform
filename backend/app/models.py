from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Wafer(Base):
    __tablename__ = 'wafers'
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String, index=True)
    created_at = Column(DateTime, default=func.now())
    test_results = relationship("TestResult", back_populates="wafer")

class TestResult(Base):
    __tablename__ = 'test_results'
    id = Column(Integer, primary_key=True, index=True)
    wafer_id = Column(Integer, ForeignKey('wafers.id'))
    die_x = Column(Integer)
    die_y = Column(Integer)
    test_name = Column(String)
    result_value = Column(Float)
    timestamp = Column(DateTime, default=func.now())
    wafer = relationship("Wafer", back_populates="test_results")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_pw = Column(String)
    role = Column(String)
