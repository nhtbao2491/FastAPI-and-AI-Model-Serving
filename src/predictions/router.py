from fastapi import APIRouter
from .schemas import PredictionRequest, PredictionResponse
from .service import make_prediction

router = APIRouter()

@router.post("/predict", )

def predict(request: PredictionRequest):
    result = make_prediction(request)
    return result