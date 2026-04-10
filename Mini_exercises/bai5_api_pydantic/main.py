from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

class PredictionRequest(BaseModel):
    area: float = Field(gt=0)
    bedrooms: int = Field(ge=0)
    bathrooms: int = Field(ge=0)

@app.post("/predict")
def predict(requests: List[PredictionRequest]):
    results = []

    for r in requests:
     
        price = r.area * 1000 + r.bedrooms * 500 + r.bathrooms * 300

        results.append({
            "features": r.model_dump(),
            "price": price
        })

    return results