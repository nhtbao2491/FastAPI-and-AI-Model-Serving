from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    area: float = Field(..., examples=[120.3], description="Diện tích nhà (m2)")
    bedrooms: int = Field(..., examples=[4], description="Số phòng ngủ")
    bathrooms: int = Field(..., examples=[4], description="Số phòng tắm")
    floors: int = Field(..., examples=[3], description="Số tầng lầu")
    property_type: str = Field(..., examples=["Villa"], description="Loại bất động sản")
    furniture: str = Field(..., examples=["Basic"], description="Tình trạng nội thất")
    legal_status: str = Field(..., examples=["Contract"], description="Tình trạng pháp lý")
    distance_to_center: int = Field(..., examples=[10], description="Khoảng cách đến trung tâm (km)")
    
    

class PredictionResponse(BaseModel):
    features: dict
    price: float = Field(..., examples=[133232.33], description="Giá nhà dự đoán")

class PredictionSummaryResponse(BaseModel):
    average_price: float = Field(..., examples=[133232.33], description="Giá nhà trung bình dự đoán")
    min_price: float = Field(..., examples=[100000.00], description="Giá nhà thấp nhất dự đoán")
    max_price: float = Field(..., examples=[150000.00], description="Giá nhà cao nhất dự đoán")
    predictions: list[dict]  