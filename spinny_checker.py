#!/usr/bin/env python3
"""
Spinny Bangalore Used Car Deal Monitor & Screener
Crawls full Bangalore inventory with zero artificial price caps.
Enriches listings with deal quality score (0-100), 2-year buyback retention, and maintenance data.
Rebuilds deals.html automatically and dispatches notifications on new finds.
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
    # German / European
    "polo", "vento", "ameo", "passat", "jetta", "taigun", "virtus", "tiguan", "t-roc", "beetle",
    "rapid", "fabia", "octavia", "superb", "kushaq", "slavia", "laura", "kodiaq", "yeti",
    # Honda
    "city", "amaze", "brio", "jazz", "wr-v", "civic", "cr-v", "elevate", "br-v", "accord",
    # Toyota
    "etios", "glanza", "yaris", "corolla", "camry", "innova", "fortuner", "hyryder", "urban cruiser",
    # Hyundai
    "i20", "elite i20", "verna", "creta", "venue", "xcent", "grand i10", "i10", "aura", "alcazar", "tucson", "elantra",
    # Maruti
    "baleno", "ciaz", "swift", "dzire", "brezza", "vitara brezza", "grand vitara", "scross", "s-cross", "ignis", "a-star", "ritz", "ertiga", "xl6", "fronx", "jimny",
    # Ford
    "ecosport", "figo", "aspire", "freestyle", "endeavour", "fiesta",
    # Tata
    "tiago", "altroz", "tigor", "zest", "nexon", "harrier", "safari", "punch", "hexa", "bolt",
    # Kia
    "seltos", "sonet", "carens", "carnival",
    # Mahindra
    "xuv300", "xuv500", "xuv700", "thar", "scorpio", "kuv100",
    # Others
    "compass", "duster", "terrano", "kiger", "magnite", "triber",
]

EXCLUDE_MODELS = [
    "alto", "eeco", "omni", "s-presso", "spresso",
    "celerio", "wagon r", "eon", "santro", "kwid", "nano", "matiz", "spark",
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
    "city": {
        "pros": ["Legendary 1.5L i-VTEC benchmark performance", "Spacious executive rear legroom", "Superb highway high-speed cruising"],
        "cons": ["Low ground clearance requires caution on tall Bangalore speed bumps", "Thin sheet metal on doors", "Basic sound insulation"],
        "maintenance_yr": "₹6,000 - ₹8,000",
        "retention_pct": 0.75,
    },
    "nexon": {
        "pros": ["5-star Global NCAP crash test rating", "Class-leading 209mm ground clearance for waterlogging", "Plush ride over potholes"],
        "cons": ["Thick A-pillar creates front-right blind spot", "AMT gearbox has noticeable shifts", "Interior panel fit can have minor gaps"],
        "maintenance_yr": "₹6,000 - ₹8,000",
        "retention_pct": 0.76,
    },
    "creta": {
        "pros": ["Unmatched resale demand in India", "Ultra-smooth petrol engine and light city controls", "Feature-loaded cabin"],
        "cons": ["Firm rear ride on sharp ruts", "Brakes have sharp initial bite", "Higher insurance renewal premiums"],
        "maintenance_yr": "₹7,000 - ₹9,500",
        "retention_pct": 0.78,
    },
    "baleno": {
        "pros": ["Extremely frugal 18-20 kmpl fuel economy", "Spacious cabin with wide rear bench", "Cheapest spare parts in segment"],
        "cons": ["Lightweight build quality", "Steering does not self-center eagerly at low speeds", "Thin paint finish"],
        "maintenance_yr": "₹4,000 - ₹5,500",
        "retention_pct": 0.78,
    },
    "ecosport": {
        "pros": ["Heavy tank-like body integrity and solid doors", "Punchy performance with direct steering feel", "High 200mm ground clearance"],
        "cons": ["Stiff low-speed suspension", "Tight rear legroom", "Ford service is independent garage reliant"],
        "maintenance_yr": "₹6,500 - ₹8,500",
        "retention_pct": 0.70,
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
    make = (car.get("make") or "").lower()
    model = (car.get("model") or "").lower()
    variant = (car.get("variant") or "").lower()
    full_name = f"{make} {model} {variant}".strip()

    if any(ex in full_name for ex in EXCLUDE_MODELS):
        return False

    if any(m in full_name for m in PRESTIGE_MODELS):
        return True

    # If it's a recognised quality manufacturer and not a excluded tin can
    reputable_makes = ["volkswagen", "honda", "toyota", "skoda", "hyundai", "ford", "tata", "kia", "mahindra", "jeep", "renault", "mg"]
    return any(rm in make for rm in reputable_makes)


def enrich_cars(cars):
    cleaned = []
    for c in cars:
        model_name = (c.get("model") or "").lower()
        matched = None
        for k in KNOWLEDGE_BASE:
            if k in model_name:
                matched = KNOWLEDGE_BASE[k]
                break
        if not matched:
            matched = {
                "pros": ["Reliable brand backing with steady resale demand", "Smooth city drivability", "Predictable routine service upkeep"],
                "cons": ["Regular periodic maintenance required"],
                "maintenance_yr": "₹5,500 - ₹7,500",
                "retention_pct": 0.72,
            }

        price = c.get("price", 0)
        km = c.get("mileage", 0)
        year = c.get("make_year", 2012)
        cat = str(c.get("procurement_category", "")).lower()
        cons_cat = str(c.get("consumer_procurement_category", "")).lower()
        is_assured = cat in ["assured", "assured-plus"] or cons_cat in ["assured", "assured-plus"]
        tier = "assured" if is_assured else "auction"

        retention_pct = matched["retention_pct"] if is_assured else round(matched["retention_pct"] * 0.90, 2)
        retention_val = round(price * retention_pct)
        total_loss_2yr = price - retention_val
        monthly_loss = round(total_loss_2yr / 24)

        # Objective Deal Quality Scoring (0 - 100)
        score = 45
        if km <= 25000: score += 24
        elif km <= 40000: score += 18
        elif km <= 60000: score += 12
        elif km <= 80000: score += 5
        elif km > 100000: score -= 10

        if year >= 2021: score += 22
        elif year >= 2019: score += 18
        elif year >= 2017: score += 12
        elif year >= 2015: score += 6
        elif year <= 2013: score -= 6

        if is_assured: score += 15

        # Value density bonus (low km relative to age)
        if year >= 2018 and km <= 40000: score += 6

        final_score = min(99, max(40, score))
        if final_score >= 80:
            deal_grade = "TOP DEAL"
        elif final_score >= 68:
            deal_grade = "VALUE PICK"
        else:
            deal_grade = "FAIR"

        pros = matched.get("pros", [])
        verdict = pros[0] if pros else "Dependable commuter with accessible service network."

        cleaned.append({
            "id": c.get("id"),
            "make": c.get("make"),
            "model": c.get("model"),
            "variant": c.get("variant"),
            "make_year": year,
            "mileage": km,
            "price": price,
            "fuel_type": c.get("fuel_type"),
            "transmission": c.get("transmission"),
            "category": tier,
            "hub": c.get("hub") or "Bangalore Hub",
            "img": c.get("showcase_image") or c.get("image"),
            "url": f"https://www.spinny.com{c.get('permanent_url', '')}",
            "deal_score": final_score,
            "deal_grade": deal_grade,
            "is_top_deal": final_score >= 68,
            "verdict": verdict,
            "analysis": {
                "pros": matched["pros"],
                "cons": matched["cons"],
                "maintenance_yr": matched["maintenance_yr"],
                "retention_pct": retention_pct,
                "est_buyback_2yr": retention_val,
                "total_loss_2yr": total_loss_2yr,
                "monthly_loss": monthly_loss,
            },
        })
    return cleaned


def fetch_cheapest_cars(city="bangalore", max_price=None, max_pages=48):
    session = requests.Session()
    session.headers.update(HEADERS)
    cars = []

    for page in range(1, max_pages + 1):
        params = {
            "city": city,
            "o": "price",
            "page": page,
        }
        if max_price is not None and max_price > 0:
            params["max_price"] = str(max_price)
        try:
            res = session.get(API_URL, params=params, timeout=12)
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
        price_ok = True if (max_price is None or max_price <= 0) else (price <= max_price)
        if price_ok and km <= 140000 and is_prestige_car(c):
            filtered.append(c)

    filtered.sort(key=lambda x: x.get("price", 0))
    return filtered


def update_deals_html(cleaned_cars):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, "clean_bangalore_cars.json")
    with open(json_path, "w") as f:
        json.dump(cleaned_cars, f, indent=2)

    try:
        with open("/tmp/clean_bangalore_cars.json", "w") as f:
            json.dump(cleaned_cars, f, indent=2)
    except Exception:
        pass

    script_path = os.path.join(cur_dir, "build_ui.py")
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path], capture_output=True)


def run_monitor(city="bangalore", max_price=None):
    cache_file = get_cache_file(city)
    seen_ids = load_seen_ids(cache_file)
    is_initial_run = len(seen_ids) == 0

    matching_cars = fetch_cheapest_cars(city=city, max_price=max_price)
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

    price_label = f"<= ₹{max_price//100000}L" if (max_price and max_price > 0) else "All Budgets"
    print(f"[{datetime.now()}] === Bangalore Deals Screener ({price_label}) — Found {len(cleaned_cars)} Cars ===")
    for idx, car in enumerate(cleaned_cars[:5], 1):
        title = f"{car.get('make_year')} {car.get('make')} {car.get('model')} {car.get('variant')}"
        price = f"₹{int(car.get('price', 0)):,}"
        km = f"{car.get('mileage', 0):,} km"
        url = car.get('url', '')
        print(f"{idx}. {title} | {price} | {km}\n   {url}")

    if not is_initial_run and new_cars:
        top_new = new_cars[0]
        title = f"{top_new.get('make_year')} {top_new.get('make')} {top_new.get('model')}"
        price = f"₹{int(top_new.get('price', 0)):,}"
        notify_mac("New Spinny Deal in Bangalore!", f"{title} for {price}")
        print(f"[{datetime.now()}] Alert dispatched for {len(new_cars)} new car(s).")
    else:
        print(f"[{datetime.now()}] Inventory refreshed. No new cars since last run.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spinny Bangalore Deals Screener & Monitor")
    parser.add_argument("--city", default="bangalore", help="Target city")
    parser.add_argument("--max-price", type=int, default=0, help="Max budget threshold (0 for unlimited)")
    args = parser.parse_args()

    max_p = None if args.max_price <= 0 else args.max_price
    run_monitor(city=args.city, max_price=max_p)
