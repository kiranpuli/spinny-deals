#!/usr/bin/env python3
"""
Hallmark Redesign for Bangalore Used Car Screener
High-density, precision data-workbench adhering to anti-AI-slop craftsmanship.
"""

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
  <title>Bangalore Used Car Market Screener · Spinny Assured &amp; Auction Intelligence</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    /* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */
    :root {
      --font-display: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif;
      --font-body: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: "JetBrains Mono", ui-monospace, monospace;

      --color-paper: #0a0c10;
      --color-surface: #11141d;
      --color-surface-hover: #161b26;
      --color-surface-inset: #0d1017;
      --color-rule: #202636;
      --color-rule-subtle: #181d29;

      --color-ink: #f8fafc;
      --color-ink-muted: #94a3b8;
      --color-ink-faint: #64748b;

      --color-cobalt: #3b82f6;
      --color-cobalt-hover: #2563eb;
      --color-cobalt-glow: rgba(59, 130, 246, 0.14);

      --color-emerald: #10b981;
      --color-emerald-bg: rgba(16, 185, 129, 0.12);
      --color-emerald-border: rgba(16, 185, 129, 0.35);

      --color-amber: #f59e0b;
      --color-amber-bg: rgba(245, 158, 11, 0.12);
      --color-amber-border: rgba(245, 158, 11, 0.35);

      --color-rose: #f43f5e;
      --color-rose-bg: rgba(244, 63, 94, 0.12);
      --color-rose-border: rgba(244, 63, 94, 0.3);

      --radius-sm: 4px;
      --radius-md: 8px;
      --radius-lg: 12px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body {
      background-color: var(--color-paper);
      color: var(--color-ink);
      font-family: var(--font-body);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      overflow-x: clip;
    }

    .shell {
      max-width: 1400px;
      margin: 0 auto;
      padding: 24px 20px 80px 20px;
    }

    /* Top Masthead */
    .masthead {
      border-bottom: 1px solid var(--color-rule);
      padding-bottom: 20px;
      margin-bottom: 24px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: flex-end;
      gap: 16px;
    }
    .masthead-title-wrap {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .masthead-eyebrow {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--color-cobalt);
      text-transform: uppercase;
      letter-spacing: 0.08em;
    }
    .masthead-title {
      font-family: var(--font-display);
      font-size: clamp(22px, 3.2vw, 32px);
      font-weight: 700;
      color: var(--color-ink);
      letter-spacing: -0.03em;
      line-height: 1.15;
    }
    .masthead-sub {
      color: var(--color-ink-muted);
      font-size: 13.5px;
    }
    .masthead-telemetry {
      display: flex;
      gap: 8px;
      align-items: center;
      flex-wrap: wrap;
    }
    .tele-tag {
      font-family: var(--font-mono);
      font-size: 11.5px;
      padding: 5px 10px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--color-rule);
      background: var(--color-surface);
      color: var(--color-ink-muted);
    }
    .tele-tag strong {
      color: var(--color-ink);
    }

    /* Workbench Filter Console */
    .filter-console {
      background: var(--color-surface);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-lg);
      padding: 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    /* Live Search Input */
    .search-row {
      display: flex;
      gap: 12px;
      align-items: center;
    }
    .search-wrap {
      position: relative;
      flex: 1;
    }
    .search-input {
      width: 100%;
      background: var(--color-surface-inset);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-md);
      padding: 11px 16px 11px 40px;
      font-family: var(--font-body);
      font-size: 14px;
      color: var(--color-ink);
      outline: none;
      transition: border-color 0.15s, box-shadow 0.15s;
    }
    .search-input:focus {
      border-color: var(--color-cobalt);
      box-shadow: 0 0 0 3px var(--color-cobalt-glow);
    }
    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--color-ink-faint);
      pointer-events: none;
      width: 16px;
      height: 16px;
    }

    /* Filter Rows */
    .filter-grid {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .filter-line {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }
    .filter-label {
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 600;
      color: var(--color-ink-faint);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      min-width: 130px;
    }
    .pill-group {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .pill {
      background: var(--color-surface-inset);
      border: 1px solid var(--color-rule);
      color: var(--color-ink-muted);
      padding: 5px 12px;
      font-size: 12.5px;
      font-weight: 500;
      border-radius: var(--radius-sm);
      cursor: pointer;
      user-select: none;
      transition: background 0.12s, border-color 0.12s, color 0.12s;
    }
    .pill:hover {
      border-color: var(--color-ink-faint);
      color: var(--color-ink);
    }
    .pill.active {
      background: var(--color-cobalt);
      border-color: var(--color-cobalt);
      color: #fff;
      font-weight: 600;
    }
    .pill.pill-assured.active {
      background: var(--color-emerald);
      border-color: var(--color-emerald);
      color: #fff;
    }
    .pill.pill-auction.active {
      background: var(--color-amber);
      border-color: var(--color-amber);
      color: #000;
    }

    /* Status Bar */
    .status-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding: 0 4px;
      font-size: 13.5px;
      color: var(--color-ink-muted);
      flex-wrap: wrap;
      gap: 12px;
    }
    .status-count {
      font-family: var(--font-mono);
      font-size: 14px;
      color: var(--color-ink);
      font-weight: 700;
    }
    .btn-reset {
      background: transparent;
      border: 1px solid var(--color-rule);
      color: var(--color-cobalt);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .btn-reset:hover {
      background: var(--color-surface-hover);
      border-color: var(--color-cobalt);
    }

    /* Cards Grid */
    .cars-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 20px;
    }
    @media (max-width: 480px) {
      .cars-grid {
        grid-template-columns: 1fr;
      }
    }

    /* Individual Car Card */
    .car-card {
      background: var(--color-surface);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: border-color 0.15s, transform 0.15s;
    }
    .car-card:hover {
      border-color: var(--color-ink-faint);
      transform: translateY(-2px);
    }

    /* Image Box */
    .card-media {
      position: relative;
      height: 205px;
      background: var(--color-surface-inset);
      display: flex;
      align-items: center;
      justify-content: center;
      border-bottom: 1px solid var(--color-rule-subtle);
    }
    .card-media img {
      max-width: 88%;
      max-height: 86%;
      object-fit: contain;
      transition: transform 0.2s ease;
    }
    .car-card:hover .card-media img {
      transform: scale(1.03);
    }

    /* Badges */
    .badge-tier {
      position: absolute;
      top: 10px;
      left: 10px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.04em;
      text-transform: uppercase;
      z-index: 2;
    }
    .badge-tier.assured {
      background: var(--color-emerald-bg);
      color: var(--color-emerald);
      border: 1px solid var(--color-emerald-border);
    }
    .badge-tier.auction {
      background: var(--color-amber-bg);
      color: var(--color-amber);
      border: 1px solid var(--color-amber-border);
    }
    .badge-hub-loc {
      position: absolute;
      bottom: 8px;
      right: 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      background: rgba(10, 12, 16, 0.85);
      border: 1px solid var(--color-rule);
      color: var(--color-ink-muted);
      padding: 2px 8px;
      border-radius: var(--radius-sm);
    }

    /* Content Area */
    .card-content {
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
      gap: 14px;
    }
    .card-header-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .card-title {
      font-family: var(--font-display);
      font-size: 18px;
      font-weight: 700;
      color: var(--color-ink);
      line-height: 1.25;
      letter-spacing: -0.01em;
    }
    .card-meta-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .chip {
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 2px 7px;
      border-radius: var(--radius-sm);
      background: var(--color-surface-inset);
      border: 1px solid var(--color-rule);
      color: var(--color-ink-muted);
      font-weight: 500;
    }

    /* Financial Matrix */
    .matrix-box {
      background: var(--color-surface-inset);
      border: 1px solid var(--color-rule-subtle);
      border-radius: var(--radius-md);
      padding: 12px;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    .matrix-cell {
      display: flex;
      flex-direction: column;
    }
    .matrix-label {
      font-family: var(--font-mono);
      font-size: 10px;
      color: var(--color-ink-faint);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .matrix-val {
      font-family: var(--font-mono);
      font-size: 15px;
      font-weight: 700;
      color: var(--color-ink);
      margin-top: 2px;
    }
    .matrix-val.price {
      color: #fff;
    }
    .matrix-val.buyback {
      color: var(--color-emerald);
    }
    .matrix-val.resale {
      color: var(--color-amber);
    }
    .matrix-val.loss {
      color: var(--color-rose);
    }
    .matrix-val.monthly {
      color: var(--color-cobalt);
    }

    /* Bangalore Dossier Accordion */
    .dossier-box {
      border-top: 1px solid var(--color-rule-subtle);
      padding-top: 12px;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .dossier-title {
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 600;
      color: var(--color-ink-faint);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    .dossier-points {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 4px;
    }
    .dossier-points li {
      font-size: 12px;
      line-height: 1.45;
      padding-left: 14px;
      position: relative;
    }
    .dossier-points.pros li {
      color: #cbd5e1;
    }
    .dossier-points.pros li::before {
      content: "+";
      position: absolute;
      left: 0;
      color: var(--color-emerald);
      font-weight: 700;
    }
    .dossier-points.cons li {
      color: #94a3b8;
    }
    .dossier-points.cons li::before {
      content: "–";
      position: absolute;
      left: 0;
      color: var(--color-rose);
      font-weight: 700;
    }

    /* Action CTA */
    .card-footer {
      border-top: 1px solid var(--color-rule-subtle);
      padding-top: 12px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 8px;
    }
    .btn-inspect {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      width: 100%;
      background: var(--color-surface-inset);
      border: 1px solid var(--color-rule);
      color: var(--color-ink);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      padding: 9px 16px;
      border-radius: var(--radius-sm);
      text-decoration: none;
      transition: all 0.15s ease;
    }
    .btn-inspect:hover {
      background: var(--color-cobalt);
      border-color: var(--color-cobalt);
      color: #fff;
    }

    .empty-state {
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      background: var(--color-surface);
      border: 1px dashed var(--color-rule);
      border-radius: var(--radius-lg);
    }
    .empty-state p {
      font-size: 15px;
      color: var(--color-ink-muted);
      margin-bottom: 16px;
    }
  </style>
</head>
<body>

  <div class="shell">
    <!-- Masthead -->
    <header class="masthead">
      <div class="masthead-title-wrap">
        <span class="masthead-eyebrow">Bangalore Market Intelligence</span>
        <h1 class="masthead-title">Used Car Valuation &amp; Buyback Screener</h1>
        <p class="masthead-sub">Live monitoring of Spinny Assured &amp; Auction wholesale inventory under ₹5.0 Lakhs with 2-year retention calculations.</p>
      </div>
      <div class="masthead-telemetry">
        <div class="tele-tag">City: <strong>Bangalore</strong></div>
        <div class="tele-tag">Tracked: <strong id="tele-total">0</strong> Cars</div>
        <div class="tele-tag">Updated: <strong>Live</strong></div>
      </div>
    </header>

    <!-- Filter Console -->
    <div class="filter-console">
      <!-- Search -->
      <div class="search-row">
        <div class="search-wrap">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <input type="text" id="filter-search" class="search-input" placeholder="Search by model, variant, brand, or hub (e.g. Polo, Automatic, Whitefield, Brio)..." oninput="onSearchChange(this.value)" />
        </div>
      </div>

      <div class="filter-grid">
        <!-- Tier Filter -->
        <div class="filter-line">
          <span class="filter-label">Listing Tier:</span>
          <div class="pill-group" id="filter-tier">
            <button class="pill active" data-key="tier" data-val="all" onclick="setFilter('tier', 'all', this)">All Deals</button>
            <button class="pill pill-assured" data-key="tier" data-val="assured" onclick="setFilter('tier', 'assured', this)">✓ Spinny Assured (Buyback)</button>
            <button class="pill pill-auction" data-key="tier" data-val="auction" onclick="setFilter('tier', 'auction', this)">⚡ Auction / Budget (Wholesale)</button>
          </div>
        </div>

        <!-- Budget Filter -->
        <div class="filter-line">
          <span class="filter-label">Max Price:</span>
          <div class="pill-group" id="filter-budget">
            <button class="pill" data-key="budget" data-val="250000" onclick="setFilter('budget', 250000, this)">&le; ₹2.5L</button>
            <button class="pill" data-key="budget" data-val="300000" onclick="setFilter('budget', 300000, this)">&le; ₹3.0L</button>
            <button class="pill" data-key="budget" data-val="350000" onclick="setFilter('budget', 350000, this)">&le; ₹3.5L</button>
            <button class="pill" data-key="budget" data-val="400000" onclick="setFilter('budget', 400000, this)">&le; ₹4.0L</button>
            <button class="pill active" data-key="budget" data-val="500000" onclick="setFilter('budget', 500000, this)">&le; ₹5.0L (All)</button>
          </div>
        </div>

        <!-- Brand Filter -->
        <div class="filter-line">
          <span class="filter-label">Brand:</span>
          <div class="pill-group" id="filter-brand">
            <button class="pill active" data-key="brand" data-val="all" onclick="setFilter('brand', 'all', this)">All</button>
            <button class="pill" data-key="brand" data-val="volkswagen" onclick="setFilter('brand', 'volkswagen', this)">Volkswagen</button>
            <button class="pill" data-key="brand" data-val="honda" onclick="setFilter('brand', 'honda', this)">Honda</button>
            <button class="pill" data-key="brand" data-val="hyundai" onclick="setFilter('brand', 'hyundai', this)">Hyundai</button>
            <button class="pill" data-key="brand" data-val="maruti" onclick="setFilter('brand', 'maruti', this)">Maruti</button>
            <button class="pill" data-key="brand" data-val="ford" onclick="setFilter('brand', 'ford', this)">Ford</button>
            <button class="pill" data-key="brand" data-val="tata" onclick="setFilter('brand', 'tata', this)">Tata</button>
            <button class="pill" data-key="brand" data-val="toyota" onclick="setFilter('brand', 'toyota', this)">Toyota</button>
          </div>
        </div>

        <!-- Transmission -->
        <div class="filter-line">
          <span class="filter-label">Gearbox:</span>
          <div class="pill-group" id="filter-trans">
            <button class="pill active" data-key="trans" data-val="all" onclick="setFilter('trans', 'all', this)">All</button>
            <button class="pill" data-key="trans" data-val="automatic" onclick="setFilter('trans', 'automatic', this)">Automatic Only</button>
            <button class="pill" data-key="trans" data-val="manual" onclick="setFilter('trans', 'manual', this)">Manual Only</button>
          </div>
        </div>

        <!-- Fuel Type -->
        <div class="filter-line">
          <span class="filter-label">Fuel:</span>
          <div class="pill-group" id="filter-fuel">
            <button class="pill active" data-key="fuel" data-val="all" onclick="setFilter('fuel', 'all', this)">All</button>
            <button class="pill" data-key="fuel" data-val="petrol" onclick="setFilter('fuel', 'petrol', this)">Petrol</button>
            <button class="pill" data-key="fuel" data-val="diesel" onclick="setFilter('fuel', 'diesel', this)">Diesel</button>
          </div>
        </div>

        <!-- Mileage Filter -->
        <div class="filter-line">
          <span class="filter-label">Max Mileage:</span>
          <div class="pill-group" id="filter-mileage">
            <button class="pill active" data-key="mileage" data-val="100000" onclick="setFilter('mileage', 100000, this)">Any KM</button>
            <button class="pill" data-key="mileage" data-val="75000" onclick="setFilter('mileage', 75000, this)">&lt; 75,000 km</button>
            <button class="pill" data-key="mileage" data-val="50000" onclick="setFilter('mileage', 50000, this)">&lt; 50,000 km</button>
            <button class="pill" data-key="mileage" data-val="30000" onclick="setFilter('mileage', 30000, this)">&lt; 30,000 km (Ultra Low)</button>
          </div>
        </div>

        <!-- Hub Location -->
        <div class="filter-line">
          <span class="filter-label">Bangalore Hub:</span>
          <div class="pill-group" id="filter-hub">
            <button class="pill active" data-key="hub" data-val="all" onclick="setFilter('hub', 'all', this)">All Hubs</button>
            <button class="pill" data-key="hub" data-val="btm" onclick="setFilter('hub', 'btm', this)">BTM (Vega City)</button>
            <button class="pill" data-key="hub" data-val="whitefield" onclick="setFilter('hub', 'whitefield', this)">Whitefield</button>
            <button class="pill" data-key="hub" data-val="malleshwaram" onclick="setFilter('hub', 'malleshwaram', this)">Malleshwaram</button>
            <button class="pill" data-key="hub" data-val="kengeri" onclick="setFilter('hub', 'kengeri', this)">Kengeri</button>
            <button class="pill" data-key="hub" data-val="electronic city" onclick="setFilter('hub', 'electronic city', this)">Electronic City</button>
            <button class="pill" data-key="hub" data-val="yelahanka" onclick="setFilter('hub', 'yelahanka', this)">Yelahanka</button>
          </div>
        </div>

        <!-- Sort By -->
        <div class="filter-line">
          <span class="filter-label">Sort Order:</span>
          <div class="pill-group" id="filter-sort">
            <button class="pill active" data-key="sort" data-val="price_asc" onclick="setFilter('sort', 'price_asc', this)">Price: Low → High</button>
            <button class="pill" data-key="sort" data-val="km_asc" onclick="setFilter('sort', 'km_asc', this)">Lowest KM</button>
            <button class="pill" data-key="sort" data-val="monthly_asc" onclick="setFilter('sort', 'monthly_asc', this)">Lowest Monthly Loss</button>
            <button class="pill" data-key="sort" data-val="year_desc" onclick="setFilter('sort', 'year_desc', this)">Newest Year</button>
            <button class="pill" data-key="sort" data-val="buyback_desc" onclick="setFilter('sort', 'buyback_desc', this)">Highest 2-Yr Buyback</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Status Bar -->
    <div class="status-bar">
      <div>
        Showing <span class="status-count" id="res-count">0</span> matching vehicles in Bangalore
      </div>
      <button class="btn-reset" onclick="resetFilters()">Reset All Filters</button>
    </div>

    <!-- Deal Cards Grid -->
    <main class="cars-grid" id="grid"></main>
  </div>

  <script>
    const ALL_CARS = """ + cars_json + """;

    const state = {
      search: '',
      tier: 'all',
      budget: 500000,
      brand: 'all',
      trans: 'all',
      fuel: 'all',
      mileage: 100000,
      hub: 'all',
      sort: 'price_asc'
    };

    document.getElementById('tele-total').textContent = ALL_CARS.length;

    function setFilter(key, val, el) {
      state[key] = val;
      const group = el.parentElement;
      group.querySelectorAll('.pill').forEach(btn => btn.classList.remove('active'));
      el.classList.add('active');
      applyFilters();
    }

    function onSearchChange(val) {
      state.search = (val || '').toLowerCase().trim();
      applyFilters();
    }

    function resetFilters() {
      state.search = '';
      state.tier = 'all';
      state.budget = 500000;
      state.brand = 'all';
      state.trans = 'all';
      state.fuel = 'all';
      state.mileage = 100000;
      state.hub = 'all';
      state.sort = 'price_asc';

      document.getElementById('filter-search').value = '';

      document.querySelectorAll('.pill-group').forEach(group => {
        group.querySelectorAll('.pill').forEach(btn => {
          const val = btn.getAttribute('data-val');
          const isDefault = (
            val === 'all' || 
            val === '500000' || 
            val === '100000' || 
            val === 'price_asc'
          );
          btn.classList.toggle('active', isDefault);
        });
      });

      applyFilters();
    }

    function applyFilters() {
      let filtered = ALL_CARS.filter(c => {
        // Search
        if (state.search) {
          const haystack = `${c.make_year} ${c.make} ${c.model} ${c.variant} ${c.hub}`.toLowerCase();
          if (!haystack.includes(state.search)) return false;
        }

        // Tier
        if (state.tier !== 'all') {
          const carTier = (c.category || 'auction').toLowerCase();
          if (carTier !== state.tier) return false;
        }

        // Budget
        if (c.price > state.budget) return false;

        // Brand
        if (state.brand !== 'all') {
          const carMake = (c.make || '').toLowerCase();
          if (!carMake.includes(state.brand)) return false;
        }

        // Transmission
        if (state.trans !== 'all') {
          const t = (c.transmission || '').toLowerCase();
          const isAuto = t.includes('auto') || t.includes('amt') || t.includes('at') || t.includes('cvt');
          if (state.trans === 'automatic' && !isAuto) return false;
          if (state.trans === 'manual' && isAuto) return false;
        }

        // Fuel
        if (state.fuel !== 'all') {
          const f = (c.fuel_type || '').toLowerCase();
          if (!f.includes(state.fuel)) return false;
        }

        // Mileage
        if (c.mileage > state.mileage) return false;

        // Hub
        if (state.hub !== 'all') {
          const h = (c.hub || '').toLowerCase();
          if (!h.includes(state.hub)) return false;
        }

        return true;
      });

      // Sorting
      if (state.sort === 'price_asc') {
        filtered.sort((a, b) => a.price - b.price);
      } else if (state.sort === 'km_asc') {
        filtered.sort((a, b) => a.mileage - b.mileage);
      } else if (state.sort === 'monthly_asc') {
        filtered.sort((a, b) => (a.analysis?.monthly_loss || 0) - (b.analysis?.monthly_loss || 0));
      } else if (state.sort === 'year_desc') {
        filtered.sort((a, b) => (b.make_year || 0) - (a.make_year || 0));
      } else if (state.sort === 'buyback_desc') {
        filtered.sort((a, b) => (b.analysis?.est_buyback_2yr || 0) - (a.analysis?.est_buyback_2yr || 0));
      }

      document.getElementById('res-count').textContent = filtered.length;
      renderGrid(filtered);
    }

    function renderGrid(cars) {
      const grid = document.getElementById('grid');
      if (cars.length === 0) {
        grid.innerHTML = `
          <div class="empty-state">
            <p>No vehicles match the selected criteria.</p>
            <button class="btn-reset" onclick="resetFilters()">Reset All Filters</button>
          </div>
        `;
        return;
      }

      grid.innerHTML = cars.map(car => {
        const isAssured = car.category === 'assured';
        const price = '₹' + Math.round(car.price).toLocaleString('en-IN');
        const km = Math.round(car.mileage).toLocaleString('en-IN') + ' km';
        const title = `${car.make_year} ${car.make} ${car.model} ${car.variant || ''}`;
        const imgUrl = car.img || '';
        const an = car.analysis || {};
        const estBuyback = '₹' + Math.round(an.est_buyback_2yr || 0).toLocaleString('en-IN');
        const totalLoss = '₹' + Math.round(an.total_loss_2yr || 0).toLocaleString('en-IN');
        const monthly = '₹' + Math.round(an.monthly_loss || 0).toLocaleString('en-IN') + '/mo';

        const tierClass = isAssured ? 'assured' : 'auction';
        const tierText = isAssured ? '✓ Spinny Assured' : '⚡ Auction / Wholesale';
        const buybackTitle = isAssured ? '2-Yr Guaranteed Buyback' : '2-Yr Est. Market Resale';
        const valClass = isAssured ? 'buyback' : 'resale';

        return `
          <article class="car-card">
            <div class="card-media">
              <span class="badge-tier ${tierClass}">${tierText}</span>
              <span class="badge-hub-loc">${car.hub}</span>
              ${imgUrl ? `<img src="${imgUrl}" alt="${title}" loading="lazy" />` : '<span style="color:var(--color-ink-faint); font-family:var(--font-mono); font-size:12px;">No Image</span>'}
            </div>
            
            <div class="card-content">
              <div class="card-header-row">
                <h2 class="card-title">${title}</h2>
                <div class="card-meta-chips">
                  <span class="chip">${km}</span>
                  <span class="chip">${(car.fuel_type || 'Petrol').toUpperCase()}</span>
                  <span class="chip">${(car.transmission || 'MT').toUpperCase()}</span>
                  ${!isAssured ? '<span class="chip" style="color:var(--color-amber); border-color:var(--color-amber-border);">Sold As-Is</span>' : ''}
                </div>
              </div>

              <!-- Financial Breakdown -->
              <div class="matrix-box">
                <div class="matrix-cell">
                  <span class="matrix-label">Listed Price</span>
                  <span class="matrix-val price">${price}</span>
                </div>
                <div class="matrix-cell">
                  <span class="matrix-label">${buybackTitle}</span>
                  <span class="matrix-val ${valClass}">${estBuyback}</span>
                </div>
                <div class="matrix-cell">
                  <span class="matrix-label">2-Yr Total Loss</span>
                  <span class="matrix-val loss">${totalLoss}</span>
                </div>
                <div class="matrix-cell">
                  <span class="matrix-label">Monthly Cost</span>
                  <span class="matrix-val monthly">${monthly}</span>
                </div>
              </div>

              <!-- Bangalore Ownership Dossier -->
              <div class="dossier-box">
                <span class="dossier-title">Bangalore Pros &amp; Cons</span>
                <ul class="dossier-points pros">
                  ${(an.pros || []).map(p => `<li>${p}</li>`).join('')}
                </ul>
                <ul class="dossier-points cons">
                  ${(an.cons || []).map(c => `<li>${c}</li>`).join('')}
                </ul>
              </div>

              <!-- CTA Button -->
              <div class="card-footer">
                <a href="${car.url || '#'}" target="_blank" rel="noopener noreferrer" class="btn-inspect">
                  Inspect Vehicle Details on Spinny &rarr;
                </a>
              </div>
            </div>
          </article>
        `;
      }).join('');
    }

    // Initial render
    applyFilters();
  </script>
</body>
</html>
"""

deals_path = os.path.join(DIR, "deals.html")
with open(deals_path, "w") as f:
    f.write(html_content)

print(f"Redesigned UI successfully written to {deals_path}")
