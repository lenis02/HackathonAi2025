from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from backend.app.db.database import Base

# 기존 Prediction 클래스는 그대로 둡니다.
class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(String, index=True)
    source_key = Column(String, index=True)
    ts = Column(DateTime, default=datetime.utcnow)
    ac_power = Column(Float)

# 아래 새로운 클래스를 추가합니다.
class FuturePrediction(Base):
    __tablename__ = "future_predictions"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(String, index=True)
    date = Column(String, index=True) # 날짜 (YYYY-MM-DD)
    daily_yield = Column(Float) # 하루 총 발전량