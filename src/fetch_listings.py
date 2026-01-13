import json
import time
import requests


API_URL = "https://api-sumyca.m2msystems.cloud/search_listings_with_room_type/location_name_and_conditions"
OUTPUT_PATH = "listings_tokyo_taito.json"
BASE_PARAMS = {
    "locationName": "日本、東京都台東区",
    "radius": 20,
    "keywordIds": "49,47", # 固定Wi-Fi / ポケットWi-Fi
    "minSize": 30,
    "minNumGuests": 2,
    "itemsPerPage": 50,
    "locale": "ja",
    # "startDate": "2025-12-12",
    # "endDate": "2026-01-11",
}

def fetch_all_listings(max_pages=None, sleep_sec=1.0):
    """
    Fetch all the listings. When running into an error, stop and return the existing data.
    """
    all_listings = []
    page = 0

    while True:
        params = dict(BASE_PARAMS)
        params["page"] = page

        print(f"\nFetching page {page} ...")

        # ---- FETCH PHASE ----
        try:
            resp = requests.get(API_URL, params=params, timeout=10)
            print("Request URL:", resp.url)
            resp.raise_for_status()       # triggers on 4xx/5xx
            data = resp.json()
        except Exception as e:
            print(f"❌ ERROR fetching page {page}: {e}")
            print("❌ Stopping early. Returning partial results.")
            return all_listings

        # ---- PARSE PHASE ----
        raw_items = data.get("listingsWithRoomType", [])
        try:
            page_listings = [item["listing"] for item in raw_items]
        except Exception as e:
            print(f"❌ ERROR parsing data on page {page}: {e}")
            print("❌ Stopping early. Returning partial results.")
            return all_listings

        # ---- CHECK FOR END ----
        if not page_listings:
            print("No more listings. Stopping.")
            break

        # ---- STORE RESULTS ----
        print(
            f"Got {len(page_listings)} listings on this page, "
            f"total so far = {len(all_listings) + len(page_listings)}"
        )
        all_listings.extend(page_listings)

        # ---- NEXT PAGE ----
        page += 1
        if max_pages is not None and page >= max_pages:
            print(f"Reached max_pages={max_pages}, stopping early.")
            break

        if sleep_sec:
            time.sleep(sleep_sec)

    return all_listings


if __name__ == "__main__":
    listings = fetch_all_listings(max_pages=60)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(listings)} listings to {OUTPUT_PATH}")
