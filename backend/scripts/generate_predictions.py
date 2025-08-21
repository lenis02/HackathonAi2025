import os
import sys
import numpy as np
import pandas as pd
import joblib
from datetime import datetime, timedelta
from sqlalchemy import desc

# --- 설정 ---
# sys.path에 프로젝트 루트 추가 (backend 폴더에서 실행한다고 가정)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal, engine
from app.models.prediction import FuturePrediction, Base
from tensorflow.keras.models import load_model

# --- 중요 설정값 ---
WINDOW_SIZE = 7       # 모델 학습 시 사용한 일 단위 시퀀스 길이
DAYS_TO_PREDICT = 7   # 며칠 예측할지

# --- 메인 실행 함수 ---
def generate_and_save_daily_predictions():
    print("🚀 하루 단위 LSTM 예측 시작")

    # 1. DB 테이블 생성 (없으면)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    print("✅ DB 세션 및 테이블 준비 완료")

    # 2. 모델 & 스케일러 로드
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "app", "ml", "lstm_daily_model.h5")
    scaler_path = os.path.join(base_dir, "app", "ml", "lstm_daily_model_with_scaler.pkl")

    try:
        model = load_model(model_path, compile=False)
        scaler_data = joblib.load(scaler_path)
        scaler = scaler_data['scaler']
        print("✅ 모델 & 스케일러 로딩 성공")
    except Exception as e:
        print(f"❌ 모델/스케일러 로딩 실패: {e}")
        db.close()
        return

    # 3. 발전소별 예측 실행
    plant_ids = ["4135001", "4136001"]  # 광주 / 남원
    today = datetime.today().date()

    for plant_id in plant_ids:
        print(f"\n=== 발전소 {plant_id} 예측 시작 ===")

        # 기존 데이터 삭제
        try:
            db.query(FuturePrediction).filter(FuturePrediction.plant_id == plant_id).delete()
            db.commit()
            print(f"기존 {plant_id} 데이터 삭제 완료")
        except Exception as e:
            print(f"⚠️ 데이터 삭제 실패: {e}")
            db.rollback()
            continue

        # (실제라면 DB의 과거 데이터를 불러와야 함)
        # 여기서는 시뮬레이션을 위해 랜덤 30일 데이터 생성
        past_days = 30
        np.random.seed(42)
        past_data = np.random.randint(2000, 8000, size=(past_days, 1))  # 과거 30일치

        if len(past_data) < WINDOW_SIZE:
            print(f"❌ 발전소 {plant_id}: 최근 {WINDOW_SIZE}일 데이터 부족")
            continue

        # 시퀀스 준비
        current_sequence = past_data[-WINDOW_SIZE:]
        current_sequence_scaled = scaler.transform(current_sequence)

        future_predictions = []

        # 7일 예측 반복
        for _ in range(DAYS_TO_PREDICT):
            reshaped_seq = current_sequence_scaled.reshape(1, WINDOW_SIZE, 1)
            next_scaled = model.predict(reshaped_seq, verbose=0)

            # 역정규화
            next_value = scaler.inverse_transform(next_scaled)[0][0]

            future_predictions.append(next_value)

            # 시퀀스 갱신
            current_sequence_scaled = np.append(current_sequence_scaled[1:], next_scaled, axis=0)

        # DataFrame 변환
        future_dates = [today + timedelta(days=i+1) for i in range(DAYS_TO_PREDICT)]
        df = pd.DataFrame({
            "date": future_dates,
            "daily_yield": future_predictions
        })

        # DB 저장 - 값을 10으로 나눠서 저장
        for _, row in df.iterrows():
            # 예측값을 10으로 나눠서 저장
            adjusted_yield = row['daily_yield'] / 10
            
            record = FuturePrediction(
                plant_id=plant_id,
                date=str(row['date']),
                daily_yield=adjusted_yield
            )
            db.add(record)
            print(f"저장: {plant_id} {row['date']} → {row['daily_yield']:.2f} → {adjusted_yield:.2f} kWh")

        db.commit()
        print(f"💾 발전소 {plant_id} 데이터 저장 완료!")

    db.close()
    print("🎉 모든 발전소 예측 완료")


if __name__ == "__main__":
    generate_and_save_daily_predictions()