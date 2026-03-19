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