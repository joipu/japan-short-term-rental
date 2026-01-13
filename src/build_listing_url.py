import json
from pathlib import Path


BASE_DIR = Path(__file__).parent
BASE_URL = "https://www.sumyca.com/listings/"
INPUT_PATH = BASE_DIR / "final.json"
OUTPUT_PATH = BASE_DIR / "final_urls.json"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    rentals = json.load(f)
urls = [BASE_URL + item["id"] for item in rentals]

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(urls, f, ensure_ascii=False, indent=2)

print(f"Saved to {OUTPUT_PATH}")