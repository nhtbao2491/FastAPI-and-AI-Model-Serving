from src.ml.model import predict_price
from src.ml.schemas import HouseFeatures
from .schemas import PredictionRequest

def make_prediction(request: PredictionRequest):
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