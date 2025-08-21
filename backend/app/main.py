from fastapi import FastAPI
from .routers import predict, result
from .db.database import Base, engine
from .models import prediction  # prediction.py에서 Prediction 클래스 import
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os


app = FastAPI()


# 앱 시작 시 테이블 생성
Base.metadata.create_all(bind=engine)

# 정적 파일 제공 (css, js, 이미지)
app.mount("/static", StaticFiles(directory="frontend/public"), name="static")

# 라우터 등록
app.include_router(predict.router)
app.include_router(result.router)

# 루트("/") → main.html
@app.get("/")
def read_root():
    file_path = os.path.join("frontend", "public", "main.html")
    return FileResponse(file_path)

# "/result" → result.html
@app.get("/result")
def read_result():
    file_path = os.path.join("frontend", "public", "result.html")
    return FileResponse(file_path)