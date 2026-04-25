from fastapi import APIRouter
from .schemas import PredictionRequest, PredictionResponse, PredictionSummaryResponse
from .service import make_batch_prediction
from .cache import get_cached, set_cached
from fastapi.concurrency import run_in_threadpool
from typing import List

router = APIRouter()


@router.post("/predict", response_model=List[PredictionResponse])
async def predict(data: List[PredictionRequest]):
    if not data:
        return []
    cached = get_cached(data)
    if cached is not None:
        return cached

    result = await run_in_threadpool(make_batch_prediction, data)

    set_cached(data, result)

    return result


@router.post("/summary", response_model=PredictionSummaryResponse)  # bỏ List[]
async def summary(data: List[PredictionRequest]):
    result = await run_in_threadpool(make_batch_prediction, data)
    
    prices = [r["price"] for r in result]
    
    return PredictionSummaryResponse(
        average_price=sum(prices) / len(prices),
        min_price=min(prices),
        max_price=max(prices),
        predictions=[
            {**data[i].model_dump(), "price": result[i]["price"]}
            for i in range(len(result))
        ]
    )
