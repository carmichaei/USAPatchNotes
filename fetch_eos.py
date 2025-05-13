# fetch_eos.py
import requests # type: ignore
import os
import json
import sys
import time
from datetime import datetime

FED_REG_LIST_API = "https://www.federalregister.gov/api/v1/documents.json"
FED_REG_DETAIL_API = "https://www.federalregister.gov/api/v1/documents/{}.json"

HEADERS = {
    "User-Agent": "USAPatchNotesBot/1.0 (https://github.com/carmichaei/USAPatchNotes)"
}

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
        response = requests.get(FED_REG_LIST_API, params=params, headers=HEADERS)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch list data: {response.status_code}")
        data = response.json()
        results = data.get("results", [])
        if not results:
            break

        for item in results:
            document_number = item.get("document_number")
            if document_number:
                detail_url = FED_REG_DETAIL_API.format(document_number)
                detail_resp = requests.get(detail_url, headers=HEADERS)
                if detail_resp.status_code == 200:
                    detail_data = detail_resp.json()
                    item["full_text_html"] = detail_data.get("body_html")
                    item["full_text_xml"] = detail_data.get("body_xml")
                time.sleep(0.5)  # prevent rate limiting on detail fetches

        eos.extend(results)
        if not data.get("next_page_url"):
            break
        page += 1
        time.sleep(1)  # prevent rate limiting on page fetches

    return eos

def save_raw_eos(eo_list, target_date):
    os.makedirs("data/raw", exist_ok=True)
    file_path = f"data/raw/eos_{target_date}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"results": eo_list}, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(eo_list)} EOs to {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fetch_eos.py YYYY-MM-DD")
        sys.exit(1)

    date_input = sys.argv[1]
    try:
        datetime.strptime(date_input, "%Y-%m-%d")  # validate date format
    except ValueError:
        print("Date must be in YYYY-MM-DD format")
        sys.exit(1)

    eos = fetch_eos_for_date(date_input)
    save_raw_eos(eos, date_input)
