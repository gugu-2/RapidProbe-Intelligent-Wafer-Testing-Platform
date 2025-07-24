from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import TestResult

router = APIRouter()

@router.get("/yield")
def get_yield_stats(db: Session = Depends(get_db)):
    total = db.query(TestResult).count()
    passes = db.query(TestResult).filter(TestResult.result_value <= 0.001).count()
    yield_rate = (passes / total * 100) if total else 0
    return {"total": total, "pass": passes, "yield": yield_rate}

@router.get("/wafer_map/{wafer_id}")
def get_wafer_map(wafer_id: int, db: Session = Depends(get_db)):
    results = db.query(TestResult).filter(TestResult.wafer_id == wafer_id).all()
    data = [{"x": r.die_x, "y": r.die_y, "status": "pass" if r.result_value <= 0.001 else "fail"} for r in results]
    return {"wafer_id": wafer_id, "die_data": data}
