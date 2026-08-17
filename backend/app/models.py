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

    departments = relationship("Department", back_populates="hospital", cascade="all, delete-orphan")
    emissions = relationship("Emission", back_populates="hospital", cascade="all, delete-orphan")
    compliance_reports = relationship("ComplianceReport", back_populates="hospital", cascade="all, delete-orphan")
    benchmarks = relationship("Benchmark", back_populates="hospital", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="hospital", cascade="all, delete-orphan")


class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    name = Column(String(50), nullable=False)

    hospital = relationship("Hospital", back_populates="departments")
    emissions = relationship("Emission", back_populates="department", cascade="all, delete-orphan")
    achievements = relationship("Achievement", back_populates="department")


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

    hospital = relationship("Hospital", back_populates="emissions")
    department = relationship("Department", back_populates="emissions")


class ComplianceReport(Base):
    __tablename__ = "compliance_reports"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    month = Column(Date, nullable=False)
    status = Column(String(20))
    notes = Column(Text)

    hospital = relationship("Hospital", back_populates="compliance_reports")


class Benchmark(Base):
    __tablename__ = "benchmarks"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    peer_group = Column(String(100))
    metric = Column(String(50))
    value = Column(Float)
    ranking = Column(Integer)

    hospital = relationship("Hospital", back_populates="benchmarks")


class Achievement(Base):
    __tablename__ = "achievements"
    id = Column(Integer, primary_key=True, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    title = Column(String(100))
    date_earned = Column(Date)

    hospital = relationship("Hospital", back_populates="achievements")
    department = relationship("Department", back_populates="achievements")
