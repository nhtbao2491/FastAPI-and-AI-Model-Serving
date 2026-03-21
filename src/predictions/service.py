from src.ml.model import predict_price, predict_batch_price
from src.ml.schemas import HouseFeatures
from .schemas import PredictionRequest
from typing import List
import pandas as pd

async def make_prediction(request: PredictionRequest):
    features = HouseFeatures(
        area = request.area,
        bedrooms = request.bedrooms,
        bathrooms = request.bathrooms,
        floors = request.floors,
        property_type = request.property_type,
        furniture = request.furniture,
        legal_status = request.legal_status,
        distance_to_center = request.distance_to_center 
    )
    prediction = predict_price(features)
    return {"price": prediction}

def make_batch_prediction(requests: List[PredictionRequest]):
    data = []
    for req in requests:
        features = HouseFeatures(
            area= req.area,
            bedrooms= req.bedrooms,
            bathrooms= req.bathrooms,
            floors= req.floors,
            property_type= req.property_type,
            furniture= req.furniture,
            legal_status= req.legal_status,
            distance_to_center= req.distance_to_center
        )
        data.append(features.model_dump())
    df = pd.DataFrame(data)
    preds = predict_batch_price(df)
    ls_results = []
    for i,p in enumerate(preds):
        ls_results.append({
            "features": data[i],
            "price": p
        })
    return ls_results
