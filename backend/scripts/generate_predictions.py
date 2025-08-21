import os
import sys
import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests # 날씨 API 요청용


# --- 설정 ---
# 프로젝트 루트의 .env 파일 로드 (API 키 등 보관)
load_dotenv() 
# sys.path에 프로젝트 루트 추가
from backend.app.db.database import SessionLocal, engine
from backend.app.models.prediction import FuturePrediction, Base

# --- OpenWeatherMap 날씨 API 함수 ---
def get_future_weather_forecast(lat, lon, days=7):
    # OpenWeatherMap One Call API 3.0 (7일 예보)
    # 참고: 90일 예보를 받으려면 유료 플랜이 필요합니다. 여기서는 7일 예보로 테스트합니다.
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("환경변수에서 OPENWEATHER_API_KEY를 찾을 수 없습니다.")
        
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=current,minutely,hourly,alerts&appid={api_key}&units=metric"
    
    response = requests.get(url)
    response.raise_for_status() # 오류 시 예외 발생
    data = response.json()['daily']

    # 15분 간격 데이터프레임 생성
    all_forecasts = []
    for day_data in data[:days]:
        date = datetime.fromtimestamp(day_data['dt']).date()
        for i in range(24 * 4): # 96 intervals of 15 mins
            ts = datetime.combine(date, datetime.min.time()) + timedelta(minutes=15 * i)
            hour = ts.hour
            # 낮 시간(6-18시)에만 일사량 존재한다고 가정
            irradiation = max(0, np.sin((hour - 6) * np.pi / 12) * 900) if 6 <= hour <= 18 else 0
            
            all_forecasts.append({
                "DATE_TIME": ts,
                "AMBIENT_TEMPERATURE": day_data['temp']['day'],
                "MODULE_TEMPERATURE": day_data['temp']['day'] + irradiation * 0.02, # 간단한 모델링
                "IRRADIATION": irradiation,
            })
            
    return pd.DataFrame(all_forecasts)

# --- 피처 엔지니어링 함수 ---
def feature_engineer_advanced(df):
    df['MINUTE'] = df['DATE_TIME'].dt.minute
    df['DAY_OF_WEEK'] = df['DATE_TIME'].dt.dayofweek
    df['HOUR_SIN'] = np.sin(2 * np.pi * df['DATE_TIME'].dt.hour / 24.0)
    df['HOUR_COS'] = np.cos(2 * np.pi * df['DATE_TIME'].dt.hour / 24.0)
    df['DOY_SIN'] = np.sin(2 * np.pi * df['DATE_TIME'].dt.dayofyear / 365.0)
    df['DOY_COS'] = np.cos(2 * np.pi * df['DATE_TIME'].dt.dayofyear / 365.0)
    return df

# --- 메인 실행 함수 ---
def generate_and_save_predictions():
    # 1. DB 테이블 생성 (없으면)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 2. 교체된 모델 로드
    model_path = os.path.join(os.path.dirname(__file__), "..", "app", "ml", "ac_power_model.pkl")
    model = joblib.load(model_path)
    
    # 3. 남원시 위경도로 미래 날씨 데이터 가져오기
    # 남원시 위도/경도: 35.4077, 127.3905
    future_weather_df = get_future_weather_forecast(lat=35.4077, lon=127.3905, days=7) # 7일치 예보
    future_features_df = feature_engineer_advanced(future_weather_df.copy())

    # 4. AC_POWER 예측
    features_for_model = model.get_booster().feature_names
    for col in features_for_model:
        if col not in future_features_df.columns:
            future_features_df[col] = 0
    
    predictions_ac = model.predict(future_features_df[features_for_model])
    predictions_ac[predictions_ac < 0] = 0
    future_weather_df['AC_POWER_PREDICTED'] = predictions_ac

    # 5. 일별 발전량(DAILY_YIELD) 집계
    future_weather_df['DATE'] = future_weather_df['DATE_TIME'].dt.date
    daily_yield = future_weather_df.groupby('DATE')['AC_POWER_PREDICTED'].sum()

    # 6. DB에 저장
    print("예측 결과를 DB에 저장합니다...")
    plant_id_namwon = "4236001" # 남원 ID
    db.query(FuturePrediction).filter(FuturePrediction.plant_id == plant_id_namwon).delete() # 기존 데이터 삭제
    
    for date, yield_value in daily_yield.items():
        record = FuturePrediction(
            plant_id=plant_id_namwon,
            date=str(date),
            daily_yield=yield_value
        )
        db.add(record)
    db.commit()
    print("저장 완료!")
    db.close()

if __name__ == "__main__":
    generate_and_save_predictions()