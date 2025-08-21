from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.app.db.database import SessionLocal
from backend.app.models.prediction import FuturePrediction
import sys, os

router = APIRouter()

# DB 세션 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get_predictions")
def get_predictions(plant_id: str, date: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)")

    # 1. 요청된 날짜의 발전량 조회
    target_day_data = db.query(FuturePrediction).filter(
        FuturePrediction.plant_id == plant_id,
        FuturePrediction.date == str(target_date)
    ).first()
    predicted_yield = target_day_data.daily_yield if target_day_data else 0

    # 2. 그래프용 8일치 데이터 조회
    start_date = target_date - timedelta(days=7)
    chart_data_query = db.query(FuturePrediction).filter(
        FuturePrediction.plant_id == plant_id,
        FuturePrediction.date >= str(start_date),
        FuturePrediction.date <= str(target_date)
    ).order_by(FuturePrediction.date).all()
    
    chart_data = [{"date": r.date, "yield": r.daily_yield} for r in chart_data_query]

    return {
        "plant_id": plant_id,
        "requested_date": str(target_date),
        "predicted_yield_for_requested_date": predicted_yield,
        "chart_data": chart_data
    }