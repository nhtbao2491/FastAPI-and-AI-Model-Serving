import asyncio
import httpx
import json
import time

URL = "http://127.0.0.1:8000/API/v1/predict"
MAX_CONCURRENT_REQUESTS = 100

with open("1000_Examples.json", "r", encoding="utf-8") as f:
    data = json.load(f)

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

# Truyền client vào để dùng chung
async def send_request(client, sample, index):
    async with semaphore:
        try:
            response = await client.post(URL, json=[sample])

            if response.status_code == 200:
                return {"index": index, "status": "success"}
            else:
                print(response.status_code, response.text)
                return {
                    "index": index,
                    "status": "error",
                    "code": response.status_code,
                    "detail": response.text
                }

        except Exception as e:
            print("EXCEPTION:", str(e))
            return {
                "index": index,
                "status": "exception",
                "error": str(e)
            }

async def main():
    print("Bắt đầu gửi request...")

    start_time = time.time()

    # Tạo 1 client duy nhất
    async with httpx.AsyncClient(timeout=60.0) as client:
        tasks = []
        for i, sample in enumerate(data):
            tasks.append(send_request(client, sample, i))


        results = await asyncio.gather(*tasks)

    end_time = time.time()

    success = sum(1 for r in results if r["status"] == "success")
    errors = len(results) - success

    print("\nKẾT QUẢ TEST")
    print(f"Tổng request: {len(results)}")
    print(f"Thành công: {success}")
    print(f"Lỗi: {errors}")
    print(f"Thời gian: {round(end_time - start_time, 2)} giây")
    print(f"RPS (request/second): {round(len(results) / (end_time - start_time), 2)}")


if __name__ == "__main__":
    asyncio.run(main())
