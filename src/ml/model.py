import joblib
import numpy as np
from .constants import MODEL_PATH, FEATURE
from .schemas import HouseFeatures

model_load = joblib.load(MODEL_PATH)

def predict_price(features: HouseFeatures) -> float:
    input_data = np.array([
        getattr(features, f) for f in FEATURE
    ]).reshape(1, -1)
    prediction =  model_load.predict(input_data)
    return float(prediction[0])