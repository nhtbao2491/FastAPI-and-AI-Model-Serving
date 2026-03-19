from fastapi import APIRouter
from .schemas import PredictionRequest, PredictionResponse
from .service import make_prediction, make_batch_prediction
from typing import List
# from src.ml.model import predict_price
router = APIRouter()

@router.post("/predict")
def predict(data: List[PredictionRequest]):
    input_data = []
    # for item in data:
    #     input_data.append({
    #         "area": item.area,
    #         "bedrooms": item.bedrooms,
    #         "bathrooms": item.bathrooms,
    #         "floors": item.floors,
    #         "property_type": item.property_type,
    #         "furniture": item.furniture,
    #         "legal_status": item.legal_status,
    #         "distance_to_center": item.distance_to_center
    #     })
    input_data = [item.model_dump() for item in data]
    prediction = make_prediction(input_data)
    return {
        "prediction" : prediction
    }

@router.post("/predict_batch")
def predict_batch(data: List[PredictionRequest]):
    predictions = make_batch_prediction(data)
    return predictions