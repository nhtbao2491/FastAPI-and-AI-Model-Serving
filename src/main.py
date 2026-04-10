from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.predictions.router import router
from src.predictions.cache import get_cache_info, clear_cache
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from src.ml.model_loader import load_model
import time
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_model()
    yield
    print("Kết thúc chương trình")


app_run = FastAPI(
    title="FastAPI và AI Model Serving",
    description="API dự đoán giá nhà",
    version="1.0",
    lifespan=lifespan
)

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app_run.include_router(
    router=router,
    prefix="/API/v1",
    tags=["Predictions"]
)


origins = [
    "http://localhost:5500"
]
app_run.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app_run.middleware("http")
async def log_time(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    # Header cho client biết response time
    response.headers["X-Response-Time"] = f"{duration:.4f}s"
    print(f"{request.method} {request.url} - {duration:.4f}s")
    return response


@app_run.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="predict.html")


@app_run.get("/API/v1/cache/info", tags=["Cache"])
def cache_info():
    """Xem trạng thái cache hiện tại."""
    return get_cache_info()

@app_run.delete("/API/v1/cache/clear", tags=["Cache"])
def cache_clear():
    """Xóa toàn bộ cache — dùng khi deploy model mới."""
    clear_cache()
    return {"message": "Cache đã được xóa."}