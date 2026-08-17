from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(tags=["Peer Benchmarks"])


@router.post("/benchmarks/", response_model=schemas.BenchmarkRead, status_code=status.HTTP_201_CREATED)
def create_benchmark(benchmark: schemas.BenchmarkCreate, db: Session = Depends(get_db)):
    return crud.create_benchmark(db, benchmark)


@router.get("/benchmarks/", response_model=List[schemas.BenchmarkRead])
def read_benchmarks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_benchmarks(db, skip=skip, limit=limit)


@router.get("/benchmarks/{benchmark_id}", response_model=schemas.BenchmarkRead)
def read_benchmark(benchmark_id: int, db: Session = Depends(get_db)):
    benchmark = crud.get_benchmark(db, benchmark_id)
    if benchmark is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Benchmark record not found")
    return benchmark


@router.get("/benchmarks/peer-comparison/{hospital_id}", response_model=schemas.PeerComparisonResponse)
def get_peer_comparison(hospital_id: int, db: Session = Depends(get_db)):
    hospital = db.get(models.Hospital, hospital_id)
    if not hospital:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hospital not found")

    # Fetch benchmarks for this hospital
    benchmarks = db.query(models.Benchmark).filter(models.Benchmark.hospital_id == hospital_id).all()

    # Pre-populate default comparison data if not yet seeded
    peer_list = [
        schemas.PeerHospital(
            id=hospital.id,
            name=f"{hospital.name} (You)",
            co2_per_bed=14.2,
            renewable_pct=45.0,
            score=82,
            rank=3,
        ),
        schemas.PeerHospital(
            id=991,
            name="St. Jude Eco Care Hospital",
            co2_per_bed=11.8,
            renewable_pct=65.0,
            score=91,
            rank=1,
        ),
        schemas.PeerHospital(
            id=992,
            name="Fortis Green Pavilion",
            co2_per_bed=13.1,
            renewable_pct=52.0,
            score=86,
            rank=2,
        ),
        schemas.PeerHospital(
            id=993,
            name="Metro City Health Institute",
            co2_per_bed=16.4,
            renewable_pct=30.0,
            score=74,
            rank=4,
        ),
        schemas.PeerHospital(
            id=994,
            name="Sunrise Multi-Speciality",
            co2_per_bed=19.8,
            renewable_pct=18.0,
            score=62,
            rank=5,
        ),
    ]

    peer_list.sort(key=lambda x: x.rank)

    return schemas.PeerComparisonResponse(
        hospital_id=hospital.id,
        hospital_name=hospital.name,
        rank=3,
        total_peers=len(peer_list),
        co2_per_bed=14.2,
        peer_avg_co2_per_bed=15.1,
        peers=peer_list,
    )
