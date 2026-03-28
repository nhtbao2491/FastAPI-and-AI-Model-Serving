from src.ml.model import predict_batch_price
from src.ml.schemas import HouseFeatures
from .schemas import PredictionRequest
from typing import List
import pandas as pd

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
