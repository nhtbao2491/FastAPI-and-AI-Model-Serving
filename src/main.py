from fastapi import FastAPI
from src.predictions.router import router

app_run = FastAPI(
    title = "FastAPI và AI Model Serving",
    description = "API dự đoán giá nhà",
    version = "1.0"
)

app_run.include_router(
    router = router,
    prefix = "/API/v1",
    tags = ["Predictions"]
)

@app_run.get("/")
def root():
    return {"msg": "FastAPI và AI Model Serving đang hoạt động"}