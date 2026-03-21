import random
import json

property_types = ["Villa", "Shophouse", "Private House", "Apartment", "Street House", "Land", "Other"]
furnitures = ["None", "Basic", "Full", "Other"]
legal_statuses = ["Has Title", "Contract", "Other"]

data = []

for _ in range(100):
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

# Xuất ra file JSON
with open("100_Examples.txt", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Đã tạo file 100_Examples.txt")