# 태양광 발전량 예측





> **목표:** 제공된 발전/센서 데이터로 **AC_POWER**를 예측해 `submit.csv`를 생성합니다.  
> **심화:** **DC_POWER** 또는 **DAILY_YIELD**도 함께 예측하면 가산점을 부여할 수 있습니다.

---

## TL;DR
- **기본 과제:** `generation_train.csv` + `sensor_train.csv`로 학습 → `generation_scoring.csv` + `sensor_scoring.csv`에 대해 **AC_POWER** 예측값 채우기.
- **DACON 데이터셋을 이용한 예시:** `example/DACON_예시_LGBM.ipynb` 또는 본 README의 **베이스라인 코드** 실행.





---



## 1) 저장소 구조
```
.
├── dataset
│   ├── generation_train.csv
│   ├── sensor_train.csv
│   └── submit
│       ├── generation_scoring.csv
│       └── sensor_scoring.csv
├── example
│   ├── DACON_예시_LGBM.ipynb
│   └── EXAMPLE_DACON
│       ├── test
│       │   ├── 0.csv ... 40.csv
│       └── train.csv
└── 시작양식.ipynb
```
- `시작양식.ipynb`: 데이터 **병합/정규화** 예시와 **제출 파일 저장** 골격이 포함되어 있습니다.
- `example/DACON_예시_LGBM.ipynb`: 간단한 **LightGBM** 예제.



---



## 2) 과제 정의
- **기본 목표:** **AC_POWER** 예측 → `submit.csv` 제출.
- **심화 목표(선택):** **DC_POWER** 또는 **DAILY_YIELD** 예측 추가.
- **권장 평가지표:** **RMSE**(Root Mean Squared Error) on AC_POWER.

>
> 시작양식 요약  
>
> - **데이터 병합**: `DATE_TIME`, `PLANT_ID` 기준으로 발전/센서 조인 → `INVERTER_ID`로 정리  
> - **제출 형식**: `submit.csv` 파일로 저장

---



## 3) 데이터 설명(스키마)
두 CSV를 **키 컬럼**으로 병합합니다.
- **공통 키:** `DATE_TIME`, `PLANT_ID`  
- **생성 데이터(generation_*) 주요 컬럼:** `SOURCE_KEY`(→ `INVERTER_ID`로 리네임), `DC_POWER`, `AC_POWER`, `DAILY_YIELD`, `TOTAL_YIELD`  
- **센서 데이터(sensor_*) 주요 컬럼:** `AMBIENT_TEMPERATURE`, `IRRADIATION`

> **P.S.:** 추가 컬럼은 자유롭게 활용하세요.

---



## 4) 제출 파일(`submit.csv`) 스키마
- **필수 컬럼:** `DATE_TIME`, `PLANT_ID`, `INVERTER_ID`, `AC_POWER`
- **선택 컬럼(심화):** `DC_POWER`, `DAILY_YIELD`
- **정렬/중복 규칙:** 키(`DATE_TIME`,`PLANT_ID`,`INVERTER_ID`) 기준 **중복 금지**. 시간 오름차순 정렬 권장.

예시:
```csv
DATE_TIME,PLANT_ID,INVERTER_ID,AC_POWER,DC_POWER,DAILY_YIELD
2020-05-15 06:00:00,1,1,123.45,0.0,0.0
2020-05-15 06:10:00,1,1,130.12,0.0,0.0
...
```





## 5) FAQ
**Q. 제출 파일은 어디에 생기는지?**  
A. 리포지터리 루트 `./submit.csv`를 기본으로 합니다.

**Q. 평가 지표는?**  
A. 기본은 `RMSE(AC_POWER)`로 가정 하시면 됩니다.
