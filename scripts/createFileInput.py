import os
import sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import random
import json
from src.config import N_REQUESTS

OUTPUT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", f"{N_REQUESTS}_Examples.json")
)

property_types = ["Villa", "Shophouse", "Private House", "Apartment", "Street House", "Land", "Other"]
furnitures = ["None", "Basic", "Full", "Other"]
legal_statuses = ["Has Title", "Contract", "Other"]

data = []
n_requests = N_REQUESTS

for _ in range(n_requests):
    item = {
        "area": round(random.uniform(30, 500), 2),
        "bedrooms": random.randint(1, 10),
        "bathrooms": random.randint(1, 10),
        "floors": random.randint(1, 5),
        "property_type": random.choice(property_types),
        "furniture": random.choice(furnitures),
        "legal_status": random.choice(legal_statuses),
        "distance_to_center": random.randint(1, 50)
    }
    data.append(item)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Đã tạo file {n_requests}_Examples.json")