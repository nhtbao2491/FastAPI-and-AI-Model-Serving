from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.predictions.router import router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app_run = FastAPI(
    title = "FastAPI và AI Model Serving",
    description = "API dự đoán giá nhà",
    version = "1.0"
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app_run.include_router(
    router = router,
    prefix = "/API/v1",
    tags = ["Predictions"]
)

# ===== CORS =====
# Sử dụng cầu lệnh python -m http.server 5500 trên terminal thứ 2 để chạy
origins = [
    "http://localhost:5500"
    #"https://fastapi-and-ai-model-serving.onrender.com",
    #["*"],
]
app_run.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
# ===== Custom Middleware =====
@app_run.middleware("http")
async def log_time(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start
    print(f"{request.method}, {request.url} - {duration:.4f}s")
    return response
# ===== API =====
@app_run.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})