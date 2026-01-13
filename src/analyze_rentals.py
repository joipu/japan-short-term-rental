import googlemaps
import json
import os
from pathlib import Path
from googlemaps.exceptions import ApiError


BASE_DIR = Path(__file__).parent
PROCESSED_PATH = BASE_DIR / "preprocessed.json"
OUTPUT_PATH = BASE_DIR / "listings_tokyo_with_amenities.json"

# Set up Google Maps
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
if not API_KEY:
    raise RuntimeError("GOOGLE_MAPS_API_KEY is not set")
gmaps = googlemaps.Client(key=API_KEY)


def load_processed_rentals():
    """Load preprocessed rentals from JSON file."""
    with open(PROCESSED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Helpers to find geocode + walking time + nearest place
def geocode_address(address: str):
    print("address: " + address)
    try:
        results = gmaps.geocode(address, language="ja", region="jp")
    except ApiError as e:
        print("Google Maps API error:", e)
        raise
    except Exception as e:
        print("Other error:", e)
        raise

    if not results:
        print("No geocode results")
        return None
    loc = results[0]["geometry"]["location"]
    return loc["lat"], loc["lng"]


def find_nearest_place(lat, lng, place_type=None, keyword=None):
    """
    Uses Places Nearby Search, ranked by distance.
    Returns the first result, or None.
    """
    response = gmaps.places_nearby(
        location=(lat, lng),
        rank_by="distance",
        type=place_type,
        keyword=keyword,
    )
    results = response.get("results", [])
    if not results:
        return None
    return results[0]


def walking_time_seconds(origin, dest):
    """
    origin, dest: (lat, lng) tuples
    """
    matrix = gmaps.distance_matrix(
        origins=[origin],
        destinations=[dest],
        mode="walking",
    )

    element = matrix["rows"][0]["elements"][0]
    if element["status"] != "OK":
        return None
    return element["duration"]["value"]  # seconds

def analyze_rental(rental):
    coords = rental.get("location", {})
    if coords is None or {}:
        # If it fails to geocode, just return basic info with False flags
        return {
            **rental,
            "has_convenience_store_7min": False,
            "has_metro_10min": False,
            "has_coworking_10min": False,
        }

    lat, lng = coords.get("lat"), coords.get("lng")
    origin = (lat, lng)

    # 1. Convenience store (t <= 7 minutes)
    convenience = find_nearest_place(lat, lng, place_type="convenience_store")
    has_convenience = False
    if convenience:
        loc = convenience["geometry"]["location"]
        dest = (loc["lat"], loc["lng"])
        t = walking_time_seconds(origin, dest)
        has_convenience = t is not None and t <= 7 * 60

    # 2. Metro / subway station (t <= 10 minutes)
    metro = find_nearest_place(lat, lng, place_type="subway_station")
    has_metro = False
    if metro:
        loc = metro["geometry"]["location"]
        dest = (loc["lat"], loc["lng"])
        t = walking_time_seconds(origin, dest)
        has_metro = t is not None and t <= 10 * 60

    # 3. Coworking space (using keyword, t <= 7 minutes)
    cowork = find_nearest_place(lat, lng, keyword="coworking space")
    if not cowork:
        # maybe also try Japanese keyword
        cowork = find_nearest_place(lat, lng, keyword="コワーキングスペース")

    has_cowork = False
    if cowork:
        loc = cowork["geometry"]["location"]
        dest = (loc["lat"], loc["lng"])
        t = walking_time_seconds(origin, dest)
        has_cowork = t is not None and t <= 10 * 60

    return {
        **rental,
        "has_convenience_store_7min": has_convenience,
        "has_metro_10min": has_metro,
        "has_coworking_10min": has_cowork,
    }


if __name__ == "__main__":
    rentals = load_processed_rentals()
    analyzed = [analyze_rental(r) for r in rentals]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(analyzed, f, ensure_ascii=False, indent=2)

    print(f"Saved to {OUTPUT_PATH}")

