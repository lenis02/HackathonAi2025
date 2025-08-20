from pydantic import BaseModel
from datetime import datetime

# 센서 입력값 (Features)
class Features(BaseModel):
    # 주변 기온 (°C)
    AMBIENT_TEMPERATURE: float
    # 모듈 표면 온도 (°C)
    MODULE_TEMPERATURE: float
    # 일사량 (W/m²)
    IRRADIATION: float

# 요청 스키마
class PredictionRequest(BaseModel):
    # 발전소 ID (region_id = PLANT_ID)
    plant_id: str
    # 센서 key
    source_key: str
    # 예측 기준 시각
    ts: datetime
    # 센서 피처
    features: Features

# 응답 스키마
class PredictionResponse(BaseModel):
    # 예측된 발전량 (AC_POWER 단위)
    AC_POWER: float
