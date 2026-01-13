import json
from pathlib import Path


# Import the listings from JSON
BASE_DIR = Path(__file__).parent
INPUT_PATH = BASE_DIR / "listings_tokyo_with_amenities.json"
OUTPUT_PATH = BASE_DIR / "final.json"

def load_rentals_with_amenities():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    filtered = [
        r for r in data
        if r["has_convenience_store_7min"]
        and r["has_metro_10min"]
        and r["has_coworking_10min"]
    ]

    print(f"Total unique rentals: {len(filtered)}")
    return filtered

filtered_listings = load_rentals_with_amenities()

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(filtered_listings, f, ensure_ascii=False, indent=2)

print(f"Saved to {OUTPUT_PATH}")
