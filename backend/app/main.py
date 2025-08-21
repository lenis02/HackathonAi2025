from fastapi import FastAPI
from backend.app.routers import predict, result, map
from backend.app.db.database import Base, engine
from backend.app.models import prediction
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
app.include_router(map.router)


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