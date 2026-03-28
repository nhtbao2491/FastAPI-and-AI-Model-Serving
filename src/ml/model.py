import joblib
import numpy as np
from .constants import MODEL_PATH, PROCESSOR_PATH
import pandas as pd

model_load = joblib.load(MODEL_PATH)
processor = joblib.load(PROCESSOR_PATH)

def predict_batch_price(df: pd.DataFrame):
    input = processor.transform(df)
    preds = model_load.predict(input)
    prices = np.expm1(preds)
    return prices
