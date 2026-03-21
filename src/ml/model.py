import joblib
import numpy as np
from .constants import MODEL_PATH, PROCESSOR_PATH, FEATURE
from .schemas import HouseFeatures
import pandas as pd

model_load = joblib.load(MODEL_PATH)
processor = joblib.load(PROCESSOR_PATH)

# def predict_price(features: HouseFeatures) -> float:
#     input_data = np.array([
#         getattr(features, f) for f in FEATURE
#     ]).reshape(1, -1)
#     prediction =  model_load.predict(input_data)
#     return float(prediction[0])

def predict_price(input_data):
    pred = pd.DataFrame(input_data)
    pred = processor.transform(pred)
    prediction =  model_load.predict(pred)
    return float(prediction[0])

def predict_batch_price(df: pd.DataFrame):
    input = processor.transform(df)
    preds = model_load.predict(input)
    prices = np.expm1(preds)
    return prices

def predict_price_batch(list_features: list) -> list:
    data = []
    for f in list_features:
        data.append({
            "area": f.area,
            "bedrooms": f.bedrooms,
            "bathrooms": f.bathrooms,
            "floors": f.floors,
            "property_type": f.property_type,
            "furniture": f.furniture,
            "legal_status": f.legal_status,
            "distance_to_center": f.distance_to_center
        })
    df = pd.DataFrame(data)
    transformed = processor.transform(df)
    predictions = model_load.predict(transformed)
    prices = np.expm1(predictions)
    return prices.tolist()