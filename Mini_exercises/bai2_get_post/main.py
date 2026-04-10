from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello")
def say_hello(name: str, age: int):
    return {
        "message": f"Hello {name}",
        "age": age
    }

@app.post("/sum")
def calculate_sum(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }


class SumRequest(BaseModel):
    a: int
    b: int

@app.post("/sum-body")
def calculate_sum_body(data: SumRequest):
    return {
        "a": data.a,
        "b": data.b,
        "result": data.a + data.b
    }