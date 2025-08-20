from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..db.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    plant_id = Column(String, index=True)
    source_key = Column(String, index=True)
    ts = Column(DateTime, default=datetime.utcnow)
    ac_power = Column(Float)
