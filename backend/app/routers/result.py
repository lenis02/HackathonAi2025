from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.prediction import Prediction

router = APIRouter()

# DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/results")
def get_results(db: Session = Depends(get_db)):
    # 최근 50개 결과만 불러오기 (원하면 전체 조회 가능)
    results = db.query(Prediction).order_by(Prediction.id.desc()).limit(50).all()
    
    return [
        {
            "id": r.id,
            "plant_id": r.plant_id,
            "source_key": r.source_key,
            "ts": r.ts,
            "ac_power": r.ac_power
        }
        for r in results
    ]
