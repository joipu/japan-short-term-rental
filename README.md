# Tokyo Rental Listings Analyzer

A small Python script project that fetches rental listings from a Japanese rental company, filters them, and enriches them with nearby amenities using the Google Maps API.

The goal is to identify rentals that are affordable, reasonably sized, and within walking distance of daily essentials.

## What it does

The pipeline performs the following steps:

1. Fetch rental listings from the provider’s public API.
2. Filter and deduplicate listings by price and layout.
3. Use Google Maps to check walkable access to:
   - Convenience stores (≤ 7 min)
   - Metro / subway stations (≤ 10 min)
   - Coworking spaces (≤ 10 min)
4. Keep only listings that satisfy all criteria.
5. Generate listing URLs for easy viewing.

## Files

- `fetch_listings.py`  
  Fetches rental listings from the API and saves them as JSON.

- `pre_process_listings.py`  
  Combines, filters, and deduplicates raw listings into `preprocessed.json`.

- `analyze_rentals.py`  
  Uses the Google Maps API to compute walking distances to nearby amenities and outputs `listings_tokyo_with_amenities.json`.

- `post_process_listings.py`  
  Filters listings that meet all amenity requirements and saves `final.json`.

- `build_listing_url.py`  
  Generates full listing URLs from `final.json`.

## Usage

Install dependencies:

```bash
pip install requests googlemaps
```

Set your Google Maps API key:
```bash
export GOOGLE_MAPS_API_KEY=your_api_key_here
```

Run the pipeline in order:
```bash
python fetch_listings.py
python pre_process_listings.py
python analyze_rentals.py
python post_process_listings.py
python build_listing_url.py
```

## Output

* `final.json` – curated rental listings
* `final_urls.json` – URLs to view the listings on the website

## Notes
* JSON files are treated as generated data artifacts.
* Google Maps API usage may incur costs.
* This project assumes Japanese location data.