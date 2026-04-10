from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Order(BaseModel):
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)

@app.post("/order")
def calculate_order(order: Order):
    total = order.price * order.quantity

    if total > 1000:
        discount = total * 0.1
    else:
        discount = 0

    return {
        "total": total,
        "discount": discount,
        "final": total - discount
    }