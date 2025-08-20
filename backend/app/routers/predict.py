from fastapi import APIRouter
from ..schemas.predict import PredictionRequest, PredictionResponse

router = APIRouter()

# 예측 요청 (POST /predict)
@router.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    """
    예측 API (현재는 더미 응답)
    """
    # 더미 응답 - 실제 모델 연결 전까지 고정 값 리턴
    return PredictionResponse(AC_POWER=1234.5)
