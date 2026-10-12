#!/usr/bin/env python3
"""
Spinny Deal Explorer Web UI
Serves a local dashboard to browse and click Spinny deals directly.
Zero third-party web framework dependencies (uses standard library http.server + requests).
"""

import http.server
import json
import socketserver
import urllib.parse
import webbrowser
import requests

PORT = 8080
API_URL = "https://api.spinny.com/v3/api/listing/v7/"

PRESTIGE_MODELS = [
    "city", "amaze", "brio", "jazz", "wr-v", "civic",
    "polo", "vento", "ameo",
    "rapid", "fabia",
    "etios", "glanza", "yaris",
    "i20", "elite i20", "verna", "creta", "venue", "xcent", "grand i10", "i10",
    "baleno", "ciaz", "swift", "dzire", "brezza", "scross", "ignis",
    "ecosport", "figo", "aspire", "freestyle"
]

EXCLUDE_MODELS = [
    "alto", "eeco", "omni", "s-presso", "spresso",
    "celerio", "wagon r", "eon", "santro", "kwid", "nano"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "origin": "https://www.spinny.com",
    "platform": "desktop",
}

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Spinny Prestige Deal Explorer</title>
  <style>
    :root {
      --bg: #0f1117;
      --card-bg: #1a1d26;
      --card-hover: #222634;
      --text: #f0f3f8;
      --subtext: #8e95a5;
      --accent: #7c3aed;
      --accent-hover: #6d28d9;
      --green: #10b981;
      --badge-bg: #272c3d;
      --border: #2a3042;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      padding: 24px;
      line-height: 1.5;
    }
    .header {
      max-width: 1200px;
      margin: 0 auto 24px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }
    .title-group h1 {
      font-size: 24px;
      font-weight: 700;
      letter-spacing: -0.5px;
    }
    .title-group p {
      color: var(--subtext);
      font-size: 14px;
    }
    .controls {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      align-items: center;
    }
    .pill-group {
      display: flex;
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 3px;
    }
    .pill-btn {
      background: none;
      border: none;
      color: var(--subtext);
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .pill-btn.active {
      background: var(--accent);
      color: #fff;
    }
    .deal-grid {
      max-width: 1200px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
    }
    .deal-card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.15s, border-color 0.15s;
    }
    .deal-card:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
    }
    .img-wrap {
      width: 100%;
      height: 190px;
      background: #14161f;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .img-wrap img {
      max-width: 90%;
      max-height: 85%;
      object-fit: contain;
    }
    .badge-buyback {
      position: absolute;
      top: 10px;
      left: 10px;
      background: rgba(16, 185, 129, 0.18);
      color: var(--green);
      border: 1px solid rgba(16, 185, 129, 0.4);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .card-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }
    .car-title {
      font-size: 17px;
      font-weight: 700;
      margin-bottom: 6px;
      color: #fff;
    }
    .meta-row {
      display: flex;
      gap: 12px;
      color: var(--subtext);
      font-size: 13px;
      margin-bottom: 14px;
    }
    .meta-tag {
      background: var(--badge-bg);
      padding: 2px 8px;
      border-radius: 4px;
    }
    .price-row {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      margin-top: auto;
      padding-top: 12px;
      border-top: 1px solid var(--border);
    }
    .price-val {
      font-size: 22px;
      font-weight: 800;
      color: #fff;
    }
    .btn-spinny {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      background: var(--accent);
      color: #fff;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      transition: background 0.15s;
    }
    .btn-spinny:hover {
      background: var(--accent-hover);
    }
    .loading-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 0;
      color: var(--subtext);
      font-size: 16px;
    }
  </style>
</head>
<body>
  <div class="header">
    <div class="title-group">
      <h1>Spinny Prestige Deal Explorer</h1>
      <p id="subheading">Strictly &le; ₹5 Lakhs &bull; Spinny Assured Guaranteed Buyback</p>
    </div>
    <div class="controls">
      <div class="pill-group" id="city-group">
        <button class="pill-btn active" onclick="setCity('bangalore')">Bangalore</button>
        <button class="pill-btn" onclick="setCity('gurgaon')">Gurgaon</button>
        <button class="pill-btn" onclick="setCity('delhi')">Delhi</button>
      </div>
      <div class="pill-group" id="budget-group">
        <button class="pill-btn" onclick="setBudget(350000)">&le; 3.5L</button>
        <button class="pill-btn" onclick="setBudget(400000)">&le; 4.0L</button>
        <button class="pill-btn active" onclick="setBudget(500000)">&le; 5.0L</button>
      </div>
    </div>
  </div>

  <div class="deal-grid" id="grid">
    <div class="loading-state">Fetching live deals from Spinny API...</div>
  </div>

  <script>
    let currentCity = 'bangalore';
    let currentBudget = 500000;

    function setCity(city) {
      currentCity = city;
      document.querySelectorAll('#city-group .pill-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.toLowerCase() === city);
      });
      loadDeals();
    }

    function setBudget(val) {
      currentBudget = val;
      document.querySelectorAll('#budget-group .pill-btn').forEach(btn => {
        const text = btn.textContent;
        const target = (val / 100000).toFixed(1);
        btn.classList.toggle('active', text.includes(target) || (val === 500000 && text.includes('5.0')));
      });
      loadDeals();
    }

    async function loadDeals() {
      const grid = document.getElementById('grid');
      grid.innerHTML = '<div class="loading-state">Loading fresh listings...</div>';
      try {
        const res = await fetch(`/api/cars?city=${currentCity}&max_price=${currentBudget}`);
        const data = await res.json();
        renderDeals(data.cars);
      } catch (err) {
        grid.innerHTML = `<div class="loading-state" style="color:#ef4444;">Failed to load deals: ${err.message}</div>`;
      }
    }

    function renderDeals(cars) {
      const grid = document.getElementById('grid');
      if (!cars || cars.length === 0) {
        grid.innerHTML = '<div class="loading-state">No matching prestige cars under this threshold currently.</div>';
        return;
      }
      grid.innerHTML = cars.map(car => {
        const price = '₹' + Math.round(car.price).toLocaleString('en-IN');
        const km = Math.round(car.mileage).toLocaleString('en-IN') + ' km';
        const imgUrl = car.without_bg_image?.file?.thumburl 
          ? (car.without_bg_image.file.thumburl.startsWith('http') ? car.without_bg_image.file.thumburl : 'https:' + car.without_bg_image.file.thumburl)
          : '';
        const title = `${car.make_year} ${car.make} ${car.model} ${car.variant || ''}`;
        const url = 'https://www.spinny.com' + (car.permanent_url || '');

        return `
          <div class="deal-card">
            <div class="img-wrap">
              <span class="badge-buyback">Assured Buyback</span>
              ${imgUrl ? `<img src="${imgUrl}" alt="${title}" loading="lazy" />` : '<span style="color:#666;">No image</span>'}
            </div>
            <div class="card-body">
              <div class="car-title">${title}</div>
              <div class="meta-row">
                <span class="meta-tag">${km}</span>
                <span class="meta-tag">${(car.fuel_type || 'Petrol').toUpperCase()}</span>
                <span class="meta-tag">${(car.transmission || 'MT').toUpperCase()}</span>
              </div>
              <div class="price-row">
                <div class="price-val">${price}</div>
                <a href="${url}" target="_blank" rel="noopener noreferrer" class="btn-spinny">View on Spinny &rarr;</a>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    loadDeals();
  </script>
</body>
</html>
"""


class SpinnyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/cars":
            qs = urllib.parse.parse_qs(parsed.query)
            city = qs.get("city", ["bangalore"])[0]
            max_price = int(qs.get("max_price", ["500000"])[0])
            cars = self.fetch_spinny_cars(city, max_price)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"cars": cars}).encode("utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))

    def fetch_spinny_cars(self, city, max_price):
        cars = []
        for page in range(1, 4):
            params = {
                "city": city,
                "product_type": "cars",
                "category": "used",
                "availability": "available,in-refurb",
                "car_category": "assured,assured-plus",
                "make": "honda,volkswagen,skoda,toyota,hyundai,maruti-suzuki,ford",
                "max_price": str(max_price),
                "o": "price",
                "page": page,
            }
            try:
                res = requests.get(API_URL, params=params, headers=HEADERS, timeout=12)
                res.raise_for_status()
                results = res.json().get("results", [])
                if not results:
                    break
                cars.extend(results)
            except Exception:
                break

        filtered = []
        for c in cars:
            price = c.get("price", 0)
            km = c.get("mileage", 0)
            make = c.get("make", "").lower()
            model = c.get("model", "").lower()
            full_name = f"{make} {model}"

            if price > max_price or km > 85000:
                continue
            if any(ex in full_name for ex in EXCLUDE_MODELS):
                continue
            if any(m in full_name for m in PRESTIGE_MODELS):
                filtered.append(c)

        filtered.sort(key=lambda x: x.get("price", 0))
        return filtered


def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SpinnyHandler) as httpd:
        print(f"Spinny UI running at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    start_server()
