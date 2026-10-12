#!/usr/bin/env python3
import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(DIR, "clean_bangalore_cars.json")
if not os.path.exists(json_path):
    json_path = "/tmp/clean_bangalore_cars.json"

with open(json_path) as f:
    cars = json.load(f)

cars_json = json.dumps(cars)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bangalore Prestige Deals &amp; 2-Year Buyback Analysis</title>
  <style>
    :root {
      --bg: #0b0d13;
      --card-bg: #141722;
      --border: #232838;
      --text: #f3f4f6;
      --subtext: #94a3b8;
      --accent: #8b5cf6;
      --accent-hover: #7c3aed;
      --green: #10b981;
      --green-bg: rgba(16, 185, 129, 0.12);
      --red: #f43f5e;
      --yellow: #f59e0b;
      --tag-bg: #1b202e;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      padding: 24px 16px;
      line-height: 1.5;
    }
    .container {
      max-width: 1240px;
      margin: 0 auto;
    }
    .header {
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 16px;
    }
    .header h1 {
      font-size: 24px;
      font-weight: 800;
      letter-spacing: -0.5px;
      color: #fff;
    }
    .header p {
      color: var(--subtext);
      font-size: 13.5px;
      margin-top: 4px;
    }
    .badge-city {
      background: var(--tag-bg);
      border: 1px solid var(--accent);
      color: var(--accent);
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 12px;
      text-transform: uppercase;
    }

    /* Filter Panel */
    .filter-panel {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 18px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .filter-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }
    .filter-label {
      font-size: 12.5px;
      color: var(--subtext);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      min-width: 110px;
    }
    .btn-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .pill {
      background: var(--tag-bg);
      border: 1px solid var(--border);
      color: var(--subtext);
      padding: 6px 14px;
      font-size: 13px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      user-select: none;
    }
    .pill:hover {
      border-color: var(--accent);
      color: #fff;
    }
    .pill.active {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }
    .status-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      font-size: 14px;
      color: var(--subtext);
    }
    .count-highlight {
      color: #fff;
      font-weight: 700;
    }
    .btn-reset {
      background: none;
      border: none;
      color: var(--accent);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      text-decoration: underline;
    }

    /* Deal Grid */
    .deal-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 22px;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: transform 0.15s, border-color 0.15s;
    }
    .card:hover {
      transform: translateY(-2px);
      border-color: var(--accent);
    }
    .img-wrap {
      width: 100%;
      height: 195px;
      background: #0e1017;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .img-wrap img {
      max-width: 86%;
      max-height: 85%;
      object-fit: contain;
    }
    .badge-buyback {
      position: absolute;
      top: 10px;
      left: 10px;
      background: var(--green-bg);
      color: var(--green);
      border: 1px solid rgba(16, 185, 129, 0.35);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }
    .badge-hub {
      position: absolute;
      bottom: 8px;
      right: 10px;
      background: rgba(0,0,0,0.6);
      color: #cbd5e1;
      font-size: 11px;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .card-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
      gap: 14px;
    }
    .car-title {
      font-size: 17.5px;
      font-weight: 700;
      color: #fff;
    }
    .meta-row {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .meta-chip {
      background: var(--tag-bg);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 12px;
      color: var(--subtext);
      font-weight: 600;
    }

    /* 2-Year Financial / Depreciation Box */
    .financials-box {
      background: #0f121b;
      border: 1px solid #1c2130;
      border-radius: 8px;
      padding: 12px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .fin-item {
      display: flex;
      flex-direction: column;
    }
    .fin-label {
      font-size: 11px;
      color: var(--subtext);
      text-transform: uppercase;
      font-weight: 600;
      letter-spacing: 0.5px;
    }
    .fin-val {
      font-size: 15px;
      font-weight: 700;
      color: #fff;
      margin-top: 2px;
    }
    .fin-val.loss { color: var(--yellow); }
    .fin-val.monthly { color: var(--green); }

    /* Pros & Cons Section */
    .analysis-box {
      background: #0e111a;
      border-radius: 8px;
      padding: 12px;
      font-size: 12.5px;
    }
    .analysis-header {
      font-weight: 700;
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .analysis-header.pros-head { color: var(--green); }
    .analysis-header.cons-head { color: var(--red); margin-top: 10px; }
    .analysis-list {
      list-style: none;
      padding: 0;
    }
    .analysis-list li {
      margin-bottom: 4px;
      color: #cbd5e1;
      padding-left: 14px;
      position: relative;
    }
    .analysis-list.pros li::before {
      content: "✔";
      position: absolute;
      left: 0;
      color: var(--green);
      font-size: 11px;
    }
    .analysis-list.cons li::before {
      content: "✖";
      position: absolute;
      left: 0;
      color: var(--red);
      font-size: 11px;
    }
    .card-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid var(--border);
      margin-top: auto;
    }
    .footer-price {
      font-size: 20px;
      font-weight: 800;
      color: #fff;
    }
    .btn-spinny {
      background: var(--accent);
      color: #fff;
      text-decoration: none;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      transition: background 0.15s;
    }
    .btn-spinny:hover {
      background: var(--accent-hover);
    }
    .empty-msg {
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 0;
      color: var(--subtext);
      font-size: 15px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div>
        <h1>Bangalore Prestige Deals &amp; 2-Year Buyback Analysis</h1>
        <p>Spinny Assured &bull; Strictly &le; ₹5 Lakhs &bull; Guaranteed Buyback &amp; Maintenance Insights</p>
      </div>
      <div>
        <span class="badge-city">City: Bangalore Only</span>
      </div>
    </div>

    <!-- Interactive Filter Panel -->
    <div class="filter-panel">
      <!-- Budget Filter -->
      <div class="filter-row">
        <span class="filter-label">Max Budget:</span>
        <div class="btn-group" id="budget-filters">
          <button class="pill" data-key="budget" data-val="350000" onclick="setFilter('budget', 350000, this)">&le; ₹3.5 Lakhs</button>
          <button class="pill" data-key="budget" data-val="400000" onclick="setFilter('budget', 400000, this)">&le; ₹4.0 Lakhs</button>
          <button class="pill" data-key="budget" data-val="450000" onclick="setFilter('budget', 450000, this)">&le; ₹4.5 Lakhs</button>
          <button class="pill active" data-key="budget" data-val="500000" onclick="setFilter('budget', 500000, this)">&le; ₹5.0 Lakhs (All)</button>
        </div>
      </div>

      <!-- Brand Filter -->
      <div class="filter-row">
        <span class="filter-label">Brand:</span>
        <div class="btn-group" id="brand-filters">
          <button class="pill active" data-key="brand" data-val="all" onclick="setFilter('brand', 'all', this)">All Brands</button>
          <button class="pill" data-key="brand" data-val="honda" onclick="setFilter('brand', 'honda', this)">Honda</button>
          <button class="pill" data-key="brand" data-val="hyundai" onclick="setFilter('brand', 'hyundai', this)">Hyundai</button>
          <button class="pill" data-key="brand" data-val="ford" onclick="setFilter('brand', 'ford', this)">Ford</button>
          <button class="pill" data-key="brand" data-val="volkswagen" onclick="setFilter('brand', 'volkswagen', this)">Volkswagen</button>
          <button class="pill" data-key="brand" data-val="skoda" onclick="setFilter('brand', 'skoda', this)">Skoda</button>
          <button class="pill" data-key="brand" data-val="maruti suzuki" onclick="setFilter('brand', 'maruti suzuki', this)">Maruti</button>
        </div>
      </div>

      <!-- Transmission Filter -->
      <div class="filter-row">
        <span class="filter-label">Transmission:</span>
        <div class="btn-group" id="trans-filters">
          <button class="pill active" data-key="trans" data-val="all" onclick="setFilter('trans', 'all', this)">All</button>
          <button class="pill" data-key="trans" data-val="automatic" onclick="setFilter('trans', 'automatic', this)">Automatic Only</button>
          <button class="pill" data-key="trans" data-val="manual" onclick="setFilter('trans', 'manual', this)">Manual Only</button>
        </div>
      </div>

      <!-- Sort Filter -->
      <div class="filter-row">
        <span class="filter-label">Sort By:</span>
        <div class="btn-group" id="sort-filters">
          <button class="pill active" data-key="sort" data-val="price" onclick="setFilter('sort', 'price', this)">Cheapest First</button>
          <button class="pill" data-key="sort" data-val="km" onclick="setFilter('sort', 'km', this)">Lowest Mileage</button>
          <button class="pill" data-key="sort" data-val="monthly" onclick="setFilter('sort', 'monthly', this)">Lowest Monthly Loss</button>
        </div>
      </div>
    </div>

    <!-- Status Bar -->
    <div class="status-bar">
      <div>Showing <span class="count-highlight" id="res-count">0</span> prestige cars in Bangalore</div>
      <button class="btn-reset" onclick="resetFilters()">Reset All Filters</button>
    </div>

    <!-- Cards Grid -->
    <div class="deal-grid" id="grid"></div>
  </div>

  <script>
    const ALL_CARS = """ + cars_json + """;

    const filters = {
      budget: 500000,
      brand: 'all',
      trans: 'all',
      sort: 'price'
    };

    function setFilter(type, val, el) {
      filters[type] = val;
      const group = el.parentElement;
      group.querySelectorAll('.pill').forEach(btn => btn.classList.remove('active'));
      el.classList.add('active');
      applyFilters();
    }

    function resetFilters() {
      filters.budget = 500000;
      filters.brand = 'all';
      filters.trans = 'all';
      filters.sort = 'price';

      document.querySelectorAll('.btn-group').forEach(group => {
        group.querySelectorAll('.pill').forEach((btn) => {
          const val = btn.getAttribute('data-val');
          const isDefault = (val === 'all' || val === '500000' || val === 'price');
          btn.classList.toggle('active', isDefault);
        });
      });
      applyFilters();
    }

    function applyFilters() {
      let filtered = ALL_CARS.filter(c => {
        // Budget
        if (c.price > filters.budget) return false;

        // Brand
        if (filters.brand !== 'all') {
          const carMake = (c.make || '').toLowerCase();
          if (!carMake.includes(filters.brand.toLowerCase())) return false;
        }

        // Transmission
        if (filters.trans !== 'all') {
          const t = (c.transmission || '').toLowerCase();
          if (filters.trans === 'automatic' && !t.includes('auto') && !t.includes('amt') && !t.includes('at') && !t.includes('cvt')) return false;
          if (filters.trans === 'manual' && (t.includes('auto') || t.includes('amt') || t.includes('at') || t.includes('cvt'))) return false;
        }

        return true;
      });

      // Sort
      if (filters.sort === 'price') {
        filtered.sort((a, b) => a.price - b.price);
      } else if (filters.sort === 'km') {
        filtered.sort((a, b) => a.mileage - b.mileage);
      } else if (filters.sort === 'monthly') {
        filtered.sort((a, b) => (a.analysis?.monthly_loss || 0) - (b.analysis?.monthly_loss || 0));
      }

      document.getElementById('res-count').textContent = filtered.length;
      renderGrid(filtered);
    }

    function renderGrid(cars) {
      const grid = document.getElementById('grid');
      if (cars.length === 0) {
        grid.innerHTML = '<div class="empty-msg">No prestige cars match the selected filters. Click "Reset All Filters" above.</div>';
        return;
      }

      grid.innerHTML = cars.map(car => {
        const price = '₹' + Math.round(car.price).toLocaleString('en-IN');
        const km = Math.round(car.mileage).toLocaleString('en-IN') + ' km';
        const imgUrl = car.img || '';
        const title = `${car.make_year} ${car.make} ${car.model} ${car.variant || ''}`;
        const url = car.url || '#';
        const an = car.analysis || {};
        const estBuyback = '₹' + Math.round(an.est_buyback_2yr || 0).toLocaleString('en-IN');
        const totalLoss = '₹' + Math.round(an.total_loss_2yr || 0).toLocaleString('en-IN');
        const monthly = '₹' + Math.round(an.monthly_loss || 0).toLocaleString('en-IN') + '/mo';

        return `
          <div class="card">
            <div class="img-wrap">
              <span class="badge-buyback">Assured Buyback</span>
              <span class="badge-hub">${car.hub}</span>
              ${imgUrl ? `<img src="${imgUrl}" alt="${title}" loading="lazy" />` : '<span style="color:#555;">No Image</span>'}
            </div>
            <div class="card-body">
              <div>
                <div class="car-title">${title}</div>
                <div class="meta-row" style="margin-top: 6px;">
                  <span class="meta-chip">${km}</span>
                  <span class="meta-chip">${(car.fuel_type || 'Petrol').toUpperCase()}</span>
                  <span class="meta-chip">${(car.transmission || 'MT').toUpperCase()}</span>
                </div>
              </div>

              <!-- 2-Year Financial / Depreciation Box -->
              <div class="financials-box">
                <div class="fin-item">
                  <span class="fin-label">2-Yr Spinny Buyback</span>
                  <span class="fin-val">${estBuyback}</span>
                </div>
                <div class="fin-item">
                  <span class="fin-label">Est. 2-Yr Net Loss</span>
                  <span class="fin-val loss">${totalLoss}</span>
                </div>
                <div class="fin-item">
                  <span class="fin-label">Monthly Depreciation</span>
                  <span class="fin-val monthly">${monthly}</span>
                </div>
                <div class="fin-item">
                  <span class="fin-label">Bangalore Maint/Yr</span>
                  <span class="fin-val">${an.maintenance_yr || '₹5,000'}</span>
                </div>
              </div>

              <!-- Pros & Cons -->
              <div class="analysis-box">
                <div class="analysis-header pros-head">Bangalore Drivability Pros</div>
                <ul class="analysis-list pros">
                  ${(an.pros || []).map(p => `<li>${p}</li>`).join('')}
                </ul>
                <div class="analysis-header cons-head">Real World Cons</div>
                <ul class="analysis-list cons">
                  ${(an.cons || []).map(c => `<li>${c}</li>`).join('')}
                </ul>
              </div>

              <div class="card-footer">
                <div class="footer-price">${price}</div>
                <a href="${url}" target="_blank" rel="noopener noreferrer" class="btn-spinny">View on Spinny &rarr;</a>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    applyFilters();
  </script>
</body>
</html>
"""

with open(os.path.join(DIR, "deals.html"), "w") as f:
    f.write(html_content)

with open(os.path.join(DIR, "index.html"), "w") as f:
    f.write(html_content)

print("Generated deals.html and index.html successfully!")
