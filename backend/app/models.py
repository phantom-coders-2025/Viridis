from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100))
    type = Column(String(50))
    beds = Column(Integer)

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String(50), nullable=False)

class Emission(Base):
    __tablename__ = "emissions"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    date = Column(Date, nullable=False)
    category = Column(String(30), nullable=False)
    subcategory = Column(String(30))
    quantity = Column(Float, nullable=False)
    unit = Column(String(10))
    emission_factor = Column(Float)
    co2e = Column(Float, nullable=False)

class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    month = Column(Date, nullable=False)
    status = Column(String(20))
    notes = Column(Text)

class Benchmark(Base):
    __tablename__ = "benchmarks"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    peer_group = Column(String(100))
    metric = Column(String(50))
    value = Column(Float)
    ranking = Column(Integer)

class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    title = Column(String(100))
    date_earned = Column(Date)
