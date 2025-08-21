from fastapi import APIRouter, Query
from backend.app.db.database import SessionLocal
from backend.app.models.prediction import FuturePrediction


router = APIRouter()

# 발전소 좌표 하드코딩
PLANT_COORDS = {
    "4135001": {"lat": 35.1741, "lng": 126.9115},  # 광주광역시 북구 용봉동
    "4136001": {"lat": 35.4064, "lng": 127.3850},  # 전북 남원시 주천면 용담리
}

@router.get("/get_map_data")
def get_map_data(date: str = Query(..., description="YYYY-MM-DD")):
    db = SessionLocal()
    results = db.query(FuturePrediction).filter(FuturePrediction.date == date).all()
    db.close()

    return [
        {
            "lat": PLANT_COORDS[r.plant_id]["lat"],
            "lng": PLANT_COORDS[r.plant_id]["lng"],
            "yield": r.daily_yield,
            "plant_id": r.plant_id
        }
        for r in results if r.plant_id in PLANT_COORDS
    ]
