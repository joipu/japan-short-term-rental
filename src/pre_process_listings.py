import json
from pathlib import Path

# Import the listings from JSON
BASE_DIR = Path(__file__).parent
JSON_GLOB = "listings_tokyo_*.json"

OUTPUT_PATH = BASE_DIR / "preprocessed.json"

def format_address(item):
    return {
        "id": item["id"],
        "layoutType": item["layoutType"],
        "totalDailyCost": item["totalDailyCost"],
        "location": item.get("location", {})
    }

def preprocess_rentals():
    """Load, combine, filter, and deduplicate listings from all matching JSON files."""
    rentals_by_id = {}  # key = listing id, value = formatted rental dict

    for json_file in BASE_DIR.glob(JSON_GLOB):
        print(f"Loading {json_file.name} ...")

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            # -------- FORMAT --------
            formatted = format_address(item)
            # -------- FILTERS --------
            if formatted["totalDailyCost"] >= 13333:
                continue  # skip expensive listings
            if formatted["layoutType"] == "1K":
                continue  # skip small studios
            # -------- DEDUP --------
            rental_id = formatted["id"]
            rentals_by_id[rental_id] = formatted

    # Convert back to list
    all_rentals = list(rentals_by_id.values())
    print(f"Total unique rentals: {len(all_rentals)}")

    return all_rentals


def save_processed_rentals(rentals, output_path=OUTPUT_PATH):
    """Save formatted rentals to JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rentals, f, ensure_ascii=False, indent=2)

    print(f"Saved processed rentals to {output_path}")


if __name__ == "__main__":
    rentals = preprocess_rentals()
    save_processed_rentals(rentals)
