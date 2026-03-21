from fastapi import APIRouter
from .schemas import PredictionRequest, PredictionResponse
from .service import make_prediction, make_batch_prediction
from fastapi.concurrency import run_in_threadpool
from typing import List
# from src.ml.model import predict_price
router = APIRouter()


@router.post("/predict")
async def predict(data: List[PredictionRequest]):
    if not data:
        return {"prediction": []}
    # Nếu nhiều sample → batch
    result = await run_in_threadpool(make_batch_prediction, data)
    return {"prediction": result}

@router.post("/predict_batch")
def predict_batch(data: List[PredictionRequest]):
    predictions = make_batch_prediction(data)
    return predictions