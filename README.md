
# FastAPI and AI Model Serving: Dự đoán giá nhà

Dự án này tập trung vào việc tìm hiểu và ứng dụng công nghệ **FastAPI** để triển khai mô hình **Trí tuệ nhân tạo (AI Model Serving)** phục vụ bài toán **dự đoán giá nhà**. Hệ thống không chỉ cung cấp các API hiệu năng cao mà còn tối ưu hóa trải nghiệm người dùng thông qua giao diện web trực quan và khả năng xử lý bất đồng bộ mạnh mẽ.

---

## Tính năng nổi bật

- **Hiệu năng cao**: Tận dụng cơ chế `async/await` của FastAPI, đạt tốc độ xử lý **>200 RPS (Requests Per Second)**.  
- **AI Model Serving chuyên nghiệp**: Mô hình `.pkl` được nạp vào RAM theo cơ chế **Singleton**, tối ưu tốc độ phản hồi.  
- **Xử lý dữ liệu thông minh**: Sử dụng **Pydantic** để validate và chuẩn hóa dữ liệu đầu vào.  
- **Caching**: Tích hợp **TTLCache** giúp giảm tải mô hình và tăng tốc request lặp lại.  
- **Tối ưu tài nguyên**: Dùng `run_in_threadpool` để xử lý tác vụ AI nặng, tránh block event loop.  
- **Giao diện trực quan**: Web UI bằng **Jinja2** + tài liệu API tự động qua **Swagger UI**.  

---

## Công nghệ sử dụng

- **Ngôn ngữ**: Python 3.11+  
- **Framework**: FastAPI  
- **Server**: Uvicorn (ASGI)  

**AI & Data**: Scikit-learn, Pandas, Numpy, Joblib  
**Khác**: Pydantic, Cachetools, Httpx, Asyncio, Postman  
**Deployment**: Render  

---

## Cấu trúc thư mục

```

fastapi-ai-model-serving/
├── src/
│   ├── ml/
│   │   ├── model.py
│   │   ├── model_loader.py
│   │   ├── schemas.py
│   │   └── constants.py
│   ├── predictions/
│   │   ├── router.py
│   │   ├── schemas.py
│   │   └── service.py
│   ├── main.py
│   └── config.py
├── models/
├── templates/
├── scripts/
├── data/
├── requirements.txt
└── README.md

````

---

## Cài đặt & chạy Local

```bash
pip install -r requirements.txt
uvicorn src.main:app_run --reload
````

* Web UI: http://127.0.0.1:8000/
* Swagger: http://127.0.0.1:8000/docs

---

##  Chạy Load Test

Để kiểm tra hiệu năng hệ thống bằng file `load_test.py`, thực hiện các bước sau:

### Bước 1: Chạy server

Mở terminal và chạy:

```bash
uvicorn src.main:app_run --reload
````

### Bước 2: Chạy script load test

Mở terminal thứ hai và chạy:

```bash
python scripts/load_test.py
```

## API

### POST `/API/v1/predict`

**Input**: JSON gồm

* diện tích, phòng ngủ, phòng tắm, số tầng
* loại nhà, nội thất, pháp lý
* khoảng cách tới trung tâm

**Output**: JSON chứa dữ liệu đầu vào + giá dự đoán
