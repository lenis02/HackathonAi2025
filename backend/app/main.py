from fastapi import FastAPI
from .routers import predict
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()


# 정적 파일 제공 (css, js, 이미지)
app.mount("/static", StaticFiles(directory="frontend/public"), name="static")

# 라우터 등록
app.include_router(predict.router)

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