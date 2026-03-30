from fastapi import APIRouter
from .schemas import PredictionRequest, PredictionResponse
from .service import make_batch_prediction
from fastapi.concurrency import run_in_threadpool
from typing import List

router = APIRouter()


@router.post("/predict", response_model= List[PredictionResponse])
async def predict(data: List[PredictionRequest]):
    if not data:
        return {"prediction": []}
    # Nếu nhiều sample → batch
    result = await run_in_threadpool(make_batch_prediction, data)
    #return {"prediction": result}
    return result