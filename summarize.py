# fetch_eos.py
import requests
import os
import json
import sys
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
    if len(sys.argv) != 2:
        print("Usage: python src/fetch_eos.py YYYY-MM-DD")
        sys.exit(1)
    date_input = sys.argv[1]
    try:
        datetime.strptime(date_input, "%Y-%m-%d")  # validate date
    except ValueError:
        print("Date must be in YYYY-MM-DD format")
        sys.exit(1)

    eos = fetch_eos_for_date(date_input)
    save_raw_eos(eos, date_input)
