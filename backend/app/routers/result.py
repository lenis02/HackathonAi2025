from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.prediction import Prediction
from datetime import datetime, timedelta

router = APIRouter()

# DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/results")
def get_results(date: str = Query(None), db: Session = Depends(get_db)):
    """
    특정 날짜 데이터만 조회 (YYYY-MM-DD)
    """
    query = db.query(Prediction)

    if date:
        try:
            # 문자열을 datetime으로 변환
            start_date = datetime.strptime(date, "%Y-%m-%d")
            end_date = start_date + timedelta(days=1)

            query = query.filter(
                Prediction.ts >= start_date,
                Prediction.ts < end_date
            )
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}

    results = query.order_by(Prediction.id.desc()).limit(50).all()

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
