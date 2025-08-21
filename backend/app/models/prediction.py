from sqlalchemy import Column, Integer, String, Float
from datetime import datetime
from backend.app.db.database import Base

# 아래 새로운 클래스를 추가합니다.
class FuturePrediction(Base):
    __tablename__ = "future_predictions"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(String, index=True)
    date = Column(String, index=True) # 날짜 (YYYY-MM-DD)
    daily_yield = Column(Float) # 하루 총 발전량