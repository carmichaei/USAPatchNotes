# fetch_eos.py
import requests
import os
import json
from datetime import datetime

FED_REG_API = "https://www.federalregister.gov/api/v1/documents.json"

def fetch_eos_for_date(target_date):
    eos = []
    page = 1
    while True:
        params = {
            "order": "newest",
            "per_page": 100,
            "page": page,
            "presidential_document_type": "executive_order",
            "publication_date[]": target_date
        }
        response = requests.get(FED_REG_API, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        data = response.json()
        results = data.get("results", [])
        if not results:
            break
        eos.extend(results)
        if not data.get("next_page_url"):
            break
        page += 1
    return eos

def save_raw_eos(eo_list, target_date):
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/eos_{target_date}.json"
    with open(file_path, "w") as f:
        json.dump({"results": eo_list}, f, indent=2)
    print(f"Saved {len(eo_list)} EOs to {file_path}")

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    eos_today = fetch_eos_for_date(today)
    save_raw_eos(eos_today, today)
