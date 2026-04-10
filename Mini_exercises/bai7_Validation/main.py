from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Product(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    price: float = Field(gt=0)
    quantity: int = Field(ge=0)

@app.post("/product")
def create_product(p: Product):
    return {
        "message": "Product created",
        "data": p
    }