# %%
# !pip install lightgbm

# %%
import pandas as pd
import numpy as np
import os
import glob
import random

import warnings
warnings.filterwarnings("ignore")

# %% [markdown]
# ## Baseline

# %%
train = pd.read_csv('./EXAMPLE_DACON/train.csv')

# %%
train.tail()

# %%
def preprocess_data(data, is_train=True):
    
    temp = data.copy()
    temp = temp[['Hour', 'TARGET', 'DHI', 'DNI', 'WS', 'RH', 'T']]

    if is_train==True:          
    
        temp['Target1'] = temp['TARGET'].shift(-48).fillna(method='ffill')
        temp['Target2'] = temp['TARGET'].shift(-48*2).fillna(method='ffill')
        temp = temp.dropna()
        
        return temp.iloc[:-96]

    elif is_train==False:
        
        temp = temp[['Hour', 'TARGET', 'DHI', 'DNI', 'WS', 'RH', 'T']]
                              
        return temp.iloc[-48:, :]


df_train = preprocess_data(train)
df_train.iloc[:48]

# %%
train.iloc[48:96]

# %%
train.iloc[48+48:96+48]

# %%
df_train.tail()

# %%
df_test = []

for i in range(41):
    file_path = './EXAMPLE_DACON/test/' + str(i) + '.csv'
    temp = pd.read_csv(file_path)
    temp = preprocess_data(temp, is_train=False)
    df_test.append(temp)

X_test = pd.concat(df_test)
X_test.shape

# %%
X_test.head(48)

# %%
df_train.head()

# %%
df_train.iloc[-48:]

# %%
from sklearn.model_selection import train_test_split
X_train_1, X_valid_1, Y_train_1, Y_valid_1 = train_test_split(df_train.iloc[:, :-2], df_train.iloc[:, -2], test_size=0.3, random_state=0)
X_train_2, X_valid_2, Y_train_2, Y_valid_2 = train_test_split(df_train.iloc[:, :-2], df_train.iloc[:, -1], test_size=0.3, random_state=0)

# %%
X_train_1.head()

# %%
X_test.head()

# %%
X_test.head()

# %%
quantiles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

# %%
from lightgbm import LGBMRegressor

# Get the model and the predictions in (a) - (b)
def LGBM(q, X_train, Y_train, X_valid, Y_valid, X_test):
    
    # (a) Modeling  
    model = LGBMRegressor(objective='quantile', alpha=q,
                         n_estimators=10000, bagging_fraction=0.7, learning_rate=0.027, subsample=0.7, force_row_wise=True )                
                         
                         
    model.fit(X_train, Y_train, eval_metric = ['quantile'], 
          eval_set=[(X_valid, Y_valid)])

    # (b) Predictions
    pred = pd.Series(model.predict(X_test).round(2))
    return pred, model

# %%
# Target 예측

def train_data(X_train, Y_train, X_valid, Y_valid, X_test):

    LGBM_models=[]
    LGBM_actual_pred = pd.DataFrame()

    for q in quantiles:
        print(q)
        pred , model = LGBM(q, X_train, Y_train, X_valid, Y_valid, X_test)
        LGBM_models.append(model)
        LGBM_actual_pred = pd.concat([LGBM_actual_pred,pred],axis=1)

    LGBM_actual_pred.columns=quantiles
    
    return LGBM_models, LGBM_actual_pred

# %%
# Target1
models_1, results_1 = train_data(X_train_1, Y_train_1, X_valid_1, Y_valid_1, X_test)
results_1.sort_index()[:48]

# %%
# Target2
models_2, results_2 = train_data(X_train_2, Y_train_2, X_valid_2, Y_valid_2, X_test)
results_2.sort_index()[:48]

# %%
results_1.sort_index().iloc[:48]

# %%
## 모델 검증 코드 ( 중복 사용 / 예시로 참고 )

# %%


# %%


# %%


# %%
results_1

# %%
models = [*models_1, *models_2]
model_quantiles = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
X_test = pd.concat([X_valid_1, X_valid_2])
Y_test = pd.concat([Y_valid_1, Y_valid_2])

results = []

for model, quantile in list(zip(models, model_quantiles)):
    pred = model.predict(X_test)
    print (quantile, len(pred), len(Y_test))
    results

# %%
from sklearn.metrics import mean_squared_error, mean_pinball_loss
import numpy as np
import pandas as pd

def _predict_best(model, X):
    num_iter = getattr(model, "best_iteration_", None)
    return model.predict(X, num_iteration=num_iter)

def evaluate_models(models, X_valid, Y_valid, target_name):
    rows = []
    # 예측 샘플 저장용
    sample_out = []

    for i, model in enumerate(models):
        q = model.get_params().get('alpha', None)  # 분위수 복원
        y_pred = _predict_best(model, X_valid)     # 반올림 금지(정밀도 유지)
        rmse = np.sqrt(mean_squared_error(Y_valid, y_pred))
        qloss = mean_pinball_loss(Y_valid, y_pred, alpha=q) if q is not None else np.nan

        rows.append({
            "target": target_name,
            "quantile": q,
            "best_iter": getattr(model, "best_iteration_", None),
            "valid_rmse": rmse,
            "valid_quantile_loss": qloss
        })

        # 예측 샘플 (상위 3개)
        sample_out.append((target_name, q, y_pred[:3].tolist()))

    metrics_df = pd.DataFrame(rows).sort_values(["target", "quantile"]).reset_index(drop=True)

    # 마지막에 모델 예측 결과 샘플 출력
    print(f"=== [{target_name}] prediction samples (first 3) ===")
    for t, q, arr in sample_out:
        print(f"target={t}, q={q} -> {arr}")

    return metrics_df

# ───────────── 평가 실행 (타겟별로 분리 평가) ─────────────
metrics_1 = evaluate_models(models_1, X_valid_1, Y_valid_1, target_name="target1")
metrics_2 = evaluate_models(models_2, X_valid_2, Y_valid_2, target_name="target2")

# 합쳐서 보기
metrics_all = pd.concat([metrics_1, metrics_2], ignore_index=True)
print("\n=== Validation Metrics (by target & quantile) ===")
print(metrics_all)

# (선택) 정렬된 표 형태로 상위 일부 확인
display(metrics_all.sort_values(["target","quantile"]).head(20))

# %%
import numpy as np
import pandas as pd

def add_composite_score(metrics_all: pd.DataFrame, 
                        w_rmse: float = 0.5, 
                        w_qloss: float = 0.5,
                        groupby_col: str = "target"):
    """
    metrics_all: columns = ['target','quantile','valid_rmse','valid_quantile_loss', ...]
    반환: score, score_0_100 컬럼 추가된 DataFrame
    """
    df = metrics_all.copy()

    # 1) 타깃별 스케일 산출(중앙값; 0/NaN 방지)
    rmse_med = df.groupby(groupby_col)['valid_rmse'].transform('median').replace({0: np.nan})
    ql_med   = df.groupby(groupby_col)['valid_quantile_loss'].transform('median').replace({0: np.nan})

    # 2) 정규화 (값이 클수록 나쁨 → 1 이상이면 중앙값보다 나쁨)
    df['RMSE_norm'] = df['valid_rmse'] / rmse_med
    df['QLoss_norm'] = df['valid_quantile_loss'] / ql_med

    # 결측/무한치 방어
    for col in ['RMSE_norm', 'QLoss_norm']:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
    df[['RMSE_norm','QLoss_norm']] = df[['RMSE_norm','QLoss_norm']].fillna(df[['RMSE_norm','QLoss_norm']].median())

    # 3) 가중 합 → 역수(높을수록 좋은 점수)
    denom = (w_rmse * df['RMSE_norm'] + w_qloss * df['QLoss_norm'])
    # 아주 드문 0 방지
    denom = denom.replace(0, denom[denom != 0].min())
    df['score'] = 1.0 / denom

    # 4) 보기 좋은 0~100 스케일(타깃별 Min-Max)
    def _mm(x):
        x_min, x_max = x.min(), x.max()
        return 100 * (x - x_min) / (x_max - x_min) if x_max > x_min else 100.0
    df['score_0_100'] = df.groupby(groupby_col)['score'].transform(_mm).round(2)

    # 5) 정렬 예시
    df = df.sort_values([groupby_col, 'score'], ascending=[True, False]).reset_index(drop=True)
    return df

# 사용 예시
metrics_all = add_composite_score(metrics_all, w_rmse=0.5, w_qloss=0.5)
score = np.mean(metrics_all['score'])


# %%
print(f"SCORE: {score}")

# %%


# %%


# %%


# %%


# %%



