import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import asyncio
import httpx
import json
import time
from src.config import MAX_CONCURRENT_REQUESTS
from src.ml.constants import FILE_NAME_TEST

URL = "http://127.0.0.1:8000/API/v1/predict"

INPUT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", f"{FILE_NAME_TEST}.json")
)

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

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
