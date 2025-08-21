import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta

# generate_predictions.py에서 피처 엔지니어링 함수를 가져옵니다.
from backend.scripts.generate_predictions import feature_engineer_advanced

def get_fake_weather_data(days=2):
    """
    테스트를 위한 '가짜' 날씨 데이터를 생성하는 함수입니다.
    실제 API 응답과 동일한 형태의 데이터프레임을 반환합니다.
    """
    print("--- 가짜 날씨 데이터 생성 시작 ---")
    base_date = datetime.now()
    future_dates = [base_date + timedelta(minutes=15 * i) for i in range(days * 24 * 4)]
    df = pd.DataFrame({'DATE_TIME': future_dates})

    # 하루 동안 해가 뜨고 지는 그럴듯한 패턴 생성
    hour = df['DATE_TIME'].dt.hour
    irradiation = np.sin((hour - 6) * np.pi / 12).clip(0) * 800 + np.random.uniform(0, 50)
    irradiation[ (hour < 6) | (hour > 18) ] = 0 # 밤 시간에는 0

    df['IRRADIATION'] = irradiation
    df['AMBIENT_TEMPERATURE'] = 25 - 10 * np.cos(hour * np.pi / 12) + np.random.uniform(-1, 1)
    df['MODULE_TEMPERATURE'] = df['AMBIENT_TEMPERATURE'] + df['IRRADIATION'] * 0.03

    print(f"--- 가짜 데이터 {len(df)}개 생성 완료 ---")
    return df

def test_model_prediction():
    """
    가짜 데이터를 사용하여 모델 로딩 및 예측 과정을 테스트하는 메인 함수
    """
    print("--- 모델 테스트 시작 ---")
    try:
        # 1. 모델 로드
        model_path = os.path.join(os.path.dirname(__file__), "..", "app", "ml", "ac_power_model.pkl")
        model = joblib.load(model_path)
        print(f"✅ 1/4: 모델 로드 성공: {model_path}")

        # 2. 가짜 데이터 생성
        fake_weather_df = get_fake_weather_data()
        print("✅ 2/4: 가짜 날씨 데이터 생성 성공")

        # 3. 피처 엔지니어링
        features_df = feature_engineer_advanced(fake_weather_df.copy())
        print("✅ 3/4: 피처 엔지니어링 성공")

        # 4. 예측 수행
        features_for_model = model.get_booster().feature_names
        for col in features_for_model:
            if col not in features_df.columns:
                features_df[col] = 0
        
        predictions = model.predict(features_df[features_for_model])
        print("✅ 4/4: 모델 예측 성공!")
        
        print("\n--- 예측 결과 (상위 10개) ---")
        print(predictions[:10])

        print("\n🎉 [성공] API 키 없이 모델 연결 및 예측 테스트를 통과했습니다! 🎉")

    except FileNotFoundError:
        print(f"❌ [실패] 모델 파일을 찾을 수 없습니다: {model_path}")
    except Exception as e:
        print(f"❌ [실패] 테스트 중 오류 발생: {e}")

if __name__ == "__main__":
    test_model_prediction()