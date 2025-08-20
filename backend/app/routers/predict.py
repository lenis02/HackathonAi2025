import os, joblib
import numpy as np
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.prediction import Prediction
from ..schemas.predict import PredictionRequest, PredictionResponse

router = APIRouter()

# DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ ML 모델 로드 (ml 폴더에서)
model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "ac_power_model.pkl")
model = joblib.load(model_path)

@router.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest, db: Session = Depends(get_db)):
    # 입력 feature → numpy 배열 변환
    features = np.array([[
        request.features.AMBIENT_TEMPERATURE,
        request.features.MODULE_TEMPERATURE,
        request.features.IRRADIATION
    ]])

    # 모델 예측
    ac_power = float(model.predict(features)[0])

    # DB 저장
    record = Prediction(
        plant_id=request.plant_id,
        source_key=request.source_key,
        ts=request.ts,
        ac_power=ac_power
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return PredictionResponse(AC_POWER=ac_power)
