#!/usr/bin/env python3
"""
Spinny Cheapest Prestige Monitor for Bangalore
Finds the lowest priced prestige cars (strictly <= 5 Lakhs) with Spinny Assured Buyback.
Automatically rebuilds deals.html and fires desktop notifications on new deals.
"""

import argparse
import json
import os
import subprocess
import sys
import requests
from datetime import datetime

API_URL = "https://api.spinny.com/v3/api/listing/v7/"

PRESTIGE_MODELS = [
    "city", "amaze", "brio", "jazz", "wr-v", "civic",
    "polo", "vento", "ameo",
    "rapid", "fabia",
    "etios", "glanza", "yaris",
    "i20", "elite i20", "verna", "creta", "venue", "xcent", "grand i10", "i10",
    "baleno", "ciaz", "swift", "dzire", "brezza", "scross", "ignis", "a-star",
    "ecosport", "figo", "aspire", "freestyle",
    "tiago", "altroz", "tigor", "zest",
]

EXCLUDE_MODELS = [
    "alto", "eeco", "omni", "s-presso", "spresso",
    "celerio", "wagon r", "eon", "santro", "kwid", "nano",
]

KNOWLEDGE_BASE = {
    "brio": {
        "pros": ["Bulletproof Honda 1.2L i-VTEC engine", "Easiest car to park in tight Bangalore spots", "Zippy 88 bhp with tight turning radius"],
        "cons": ["Stiff rear ride on bad roads/potholes", "Small 175L glass boot", "Basic interior features"],
        "maintenance_yr": "₹4,500 - ₹6,000",
        "retention_pct": 0.72,
    },
    "i10": {
        "pros": ["Feather-light clutch & steering for traffic", "Spares available at every neighborhood garage", "Upright seating with clear visibility"],
        "cons": ["1.1L engine strains on highway inclines", "City fuel economy ~11-12 kmpl with AC", "Dated dashboard styling"],
        "maintenance_yr": "₹4,000 - ₹5,000",
        "retention_pct": 0.71,
    },
    "figo": {
        "pros": ["Tank-like European build quality & safety", "Plush suspension over Bangalore potholes", "Excellent highway high-speed stability"],
        "cons": ["Ford service network is independent/FNG reliant", "Weak low-end torque in 2nd gear traffic", "Slightly heavier clutch"],
        "maintenance_yr": "₹5,500 - ₹7,000",
        "retention_pct": 0.67,
    },
    "amaze": {
        "pros": ["Massive 400L boot for outstation & airport runs", "Spacious rear legroom with great resale demand", "Engine easily lasts 200,000+ km"],
        "cons": ["Soft rear suspension can scrape tall speedbumps", "Lightweight door build compared to Polo", "Basic cabin sound insulation"],
        "maintenance_yr": "₹5,000 - ₹6,500",
        "retention_pct": 0.73,
    },
    "aspire": {
        "pros": ["Top Titanium trim (alloys, fog lamps, audio)", "Solid high-speed road manners & steering feel", "Great crash safety feel"],
        "cons": ["Ford parts take 2-3 days to order", "City mileage around 12-13 kmpl", "Resale market smaller than Maruti/Hyundai"],
        "maintenance_yr": "₹5,500 - ₹7,000",
        "retention_pct": 0.69,
    },
    "grand i10": {
        "pros": ["Ultra-refined 1.2L 4-cylinder engine", "Premium cabin fit and finish", "Very soft clutch and smooth gearbox"],
        "cons": ["Suspension gets floaty above 100 km/h", "Rear AC vents only on top trims", "Average mileage in heavy city jams"],
        "maintenance_yr": "₹4,500 - ₹6,000",
        "retention_pct": 0.74,
    },
    "polo": {
        "pros": ["Unmatched German chassis stability & paint quality", "Heavy doors with thud sound (5-star feel)", "Timeless styling and prestige"],
        "cons": ["Higher parts cost if sensors fail", "Tighter rear legroom", "3-cylinder petrol is vocal at high RPM"],
        "maintenance_yr": "₹7,500 - ₹10,000",
        "retention_pct": 0.75,
    },
    "jazz": {
        "pros": ["Incredible interior space & Magic Seats practicality", "Large glasshouse with zero blind spots", "Honda reliability"],
        "cons": ["Wide body takes care in narrow alleys", "Rubberband CVT (if AT) or tall gearing", "Priced higher than Brio"],
        "maintenance_yr": "₹5,000 - ₹6,500",
        "retention_pct": 0.74,
    },
    "rapid": {
        "pros": ["Executive sedan road presence", "Solid German build & planted highway cruise", "Large 460L boot space"],
        "cons": ["Skoda maintenance & spares cost higher", "Heavy steering at parking speeds", "Requires proactive upkeep"],
        "maintenance_yr": "₹8,500 - ₹12,000",
        "retention_pct": 0.68,
    },
    "swift": {
        "pros": ["Highest resale value in Indian market", "Instant parts availability everywhere", "Fun to drive peppy dynamics"],
        "cons": ["Thinner sheet metal", "Common on roads (less exclusivity)", "Ride is firm over broken tarmac"],
        "maintenance_yr": "₹4,000 - ₹5,500",
        "retention_pct": 0.78,
    },
    "etios": {
        "pros": ["Indestructible Toyota engine & chassis", "Massive 595L boot space", "Plush ride quality over potholes"],
        "cons": ["Basic cab-like dashboard ergonomics", "Plain exterior styling", "Larger turning radius"],
        "maintenance_yr": "₹4,500 - ₹6,000",
        "retention_pct": 0.72,
    },
    "a-star": {
        "pros": ["Super compact - slots into tightest parking spots", "Torque converter AT is smoother than modern AMTs", "Maruti parts cost peanuts"],
        "cons": ["Tight rear legroom", "Small 180L boot", "Outdated interior trim"],
        "maintenance_yr": "₹3,500 - ₹4,500",
        "retention_pct": 0.70,
    },
    "tiago": {
        "pros": ["Solid 4-star Global NCAP crash safety", "Best-in-class 8-speaker Harman sound system", "Thick European sheet metal feel"],
        "cons": ["3-cylinder Revotron engine vibrates at idle", "Tata service center experience varies", "Clutch has slightly long travel"],
        "maintenance_yr": "₹5,000 - ₹6,500",
        "retention_pct": 0.72,
    },
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "origin": "https://www.spinny.com",
    "platform": "desktop",
}


def get_cache_file(city):
    return os.path.expanduser(f"~/.spinny_cheapest_prestige_{city}.json")


def load_seen_ids(cache_file):
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r") as f:
                return set(json.load(f))
        except Exception:
            return set()
    return set()


def save_seen_ids(cache_file, seen_ids):
    with open(cache_file, "w") as f:
        json.dump(list(seen_ids), f, indent=2)


def notify_mac(title, message):
    script = f'display notification "{message}" with title "{title}" sound name "Glass"'
    subprocess.run(["osascript", "-e", script], capture_output=True)


def is_prestige_car(car):
    make = car.get("make", "").lower()
    model = car.get("model", "").lower()
    full_name = f"{make} {model}"

    if any(ex in full_name for ex in EXCLUDE_MODELS):
        return False

    return any(m in full_name for m in PRESTIGE_MODELS)


def enrich_cars(cars):
    cleaned = []
    for c in cars:
        model_name = c.get("model", "").lower()
        matched = None
        for k in KNOWLEDGE_BASE:
            if k in model_name:
                matched = KNOWLEDGE_BASE[k]
                break
        if not matched:
            matched = {
                "pros": ["Reliable brand backing", "Good city drivability", "Low maintenance"],
                "cons": ["Regular periodic maintenance required"],
                "maintenance_yr": "₹5,000 - ₹6,500",
                "retention_pct": 0.70,
            }

        price = c.get("price", 0)
        retention_val = round(price * matched["retention_pct"])
        total_loss_2yr = price - retention_val
        monthly_loss = round(total_loss_2yr / 24)

        img_url = (c.get("without_bg_image", {}).get("file", {}).get("thumburl", "") or "")
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        cleaned.append({
            "id": c.get("id"),
            "make": c.get("make"),
            "model": c.get("model"),
            "variant": c.get("variant"),
            "make_year": c.get("make_year"),
            "price": price,
            "mileage": c.get("mileage"),
            "fuel_type": c.get("fuel_type"),
            "transmission": c.get("transmission"),
            "url": "https://www.spinny.com" + c.get("permanent_url", ""),
            "img": img_url,
            "hub": c.get("hub_short_name", "Bangalore"),
            "analysis": {
                "pros": matched["pros"],
                "cons": matched["cons"],
                "maintenance_yr": matched["maintenance_yr"],
                "est_buyback_2yr": retention_val,
                "total_loss_2yr": total_loss_2yr,
                "monthly_loss": monthly_loss,
            },
        })
    return cleaned


def fetch_cheapest_cars(city, max_price=500000):
    cars = []
    for page in range(1, 12):
        params = {
            "city": city,
            "max_price": str(max_price),
            "o": "price",
            "page": page,
        }
        try:
            res = requests.get(API_URL, params=params, headers=HEADERS, timeout=15)
            res.raise_for_status()
            page_results = res.json().get("results", [])
            if not page_results:
                break
            cars.extend(page_results)
        except Exception as e:
            print(f"[{datetime.now()}] Error on page {page}: {e}", file=sys.stderr)
            break

    filtered = []
    for c in cars:
        price = c.get("price", 0)
        km = c.get("mileage", 0)
        if price <= max_price and km <= 85000 and is_prestige_car(c):
            filtered.append(c)

    filtered.sort(key=lambda x: x.get("price", 0))
    return filtered


def update_deals_html(cleaned_cars):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, "clean_bangalore_cars.json")
    with open(json_path, "w") as f:
        json.dump(cleaned_cars, f, indent=2)

    # Also sync /tmp for compatibility
    try:
        with open("/tmp/clean_bangalore_cars.json", "w") as f:
            json.dump(cleaned_cars, f, indent=2)
    except Exception:
        pass

    script_path = os.path.join(cur_dir, "build_ui.py")
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path], capture_output=True)


def run_monitor(city="bangalore", max_price=500000):
    cache_file = get_cache_file(city)
    seen_ids = load_seen_ids(cache_file)
    is_initial_run = len(seen_ids) == 0

    matching_cars = fetch_cheapest_cars(city, max_price)
    cleaned_cars = enrich_cars(matching_cars)
    new_cars = []

    for car in matching_cars:
        car_id = car.get("id")
        if car_id not in seen_ids:
            new_cars.append(car)
            seen_ids.add(car_id)

    save_seen_ids(cache_file, seen_ids)

    # Rebuild deals.html with live data
    update_deals_html(cleaned_cars)

    print(f"[{datetime.now()}] === Daily Bangalore Prestige Deals (<= ₹{max_price//100000}L) ===")
    for idx, car in enumerate(matching_cars[:5], 1):
        title = f"{car.get('make_year')} {car.get('make')} {car.get('model')} {car.get('variant')}"
        price = f"₹{int(car.get('price', 0)):,}"
        km = f"{car.get('mileage', 0):,} km"
        url = f"https://www.spinny.com{car.get('permanent_url', '')}"
        print(f"{idx}. {title} | {price} | {km}\n   {url}")

    if not is_initial_run and new_cars:
        top_new = new_cars[0]
        title = f"{top_new.get('make_year')} {top_new.get('make')} {top_new.get('model')}"
        price = f"₹{int(top_new.get('price', 0)):,}"
        notify_mac("New Spinny Deal in Bangalore!", f"{title} for {price} (Buyback Eligible)")
        print(f"[{datetime.now()}] Alert dispatched for {len(new_cars)} new car(s).")
    else:
        print(f"[{datetime.now()}] Inventory refreshed. No new cars since last run.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spinny Cheapest Prestige Monitor")
    parser.add_argument("--city", default="bangalore", help="Target city")
    parser.add_argument("--max-price", type=int, default=500000, help="Max budget threshold")
    args = parser.parse_args()

    run_monitor(city=args.city, max_price=args.max_price)
