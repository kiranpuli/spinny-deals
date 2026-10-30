#!/usr/bin/env python3
"""
Hallmark Redesign — Minimal, Debloated Used Car Screener
Theme: Cobalt (Modern-Minimal / Precision Workbench)
Discipline: Anti-AI-slop, zero card-in-card nesting, single-deck workbench controls, honest data.
"""

import json
import os
import shutil

DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(DIR, "clean_bangalore_cars.json")
if not os.path.exists(json_path):
    json_path = "/tmp/clean_bangalore_cars.json"

if os.path.exists(json_path):
    with open(json_path) as f:
        cars = json.load(f)
else:
    cars = []

# Ensure consistent deal scoring & concise verdicts
for c in cars:
    year = c.get("make_year", 2012)
    km = c.get("mileage", 100000)
    price = c.get("price", 500000)
    is_assured = c.get("category") == "assured"

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
    if year >= 2018 and km <= 40000: score += 6

    final_score = min(99, max(40, score))
    c["deal_score"] = final_score
    c["is_top_deal"] = final_score >= 68
    c["deal_grade"] = "TOP DEAL" if final_score >= 80 else ("VALUE PICK" if final_score >= 68 else "FAIR")

    pros = c.get("analysis", {}).get("pros", [])
    if pros:
        c["verdict"] = pros[0]
    else:
        c["verdict"] = "Reliable city commuter with steady resale value."

cars_json = json.dumps(cars)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bangalore Used Cars · Hallmark Screener</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600;700&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">
  <style>
    /* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */
    :root {
      --font-display: "Space Grotesk", -apple-system, sans-serif;
      --font-body: "Inter", -apple-system, sans-serif;
      --font-mono: "JetBrains Mono", ui-monospace, monospace;

      --color-paper: #090d16;
      --color-surface: #101622;
      --color-surface-hover: #141c2c;
      --color-rule: #1e283d;
      --color-rule-subtle: #151d2c;

      --color-ink: #f8fafc;
      --color-ink-muted: #94a3b8;
      --color-ink-faint: #64748b;

      --color-cobalt: #3b82f6;
      --color-cobalt-glow: rgba(59, 130, 246, 0.16);
      --color-emerald: #10b981;
      --color-emerald-bg: rgba(16, 185, 129, 0.14);
      --color-amber: #f59e0b;
      --color-amber-bg: rgba(245, 158, 11, 0.14);

      --radius-sm: 4px;
      --radius-md: 6px;
      --radius-lg: 10px;
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
      max-width: 1380px;
      margin: 0 auto;
      padding: 24px 20px 80px 20px;
    }

    /* Masthead */
    .masthead {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      flex-wrap: wrap;
      gap: 16px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--color-rule);
      margin-bottom: 20px;
    }
    .masthead-title {
      font-family: var(--font-display);
      font-size: clamp(22px, 3vw, 28px);
      font-weight: 700;
      letter-spacing: -0.02em;
      color: var(--color-ink);
    }
    .masthead-sub {
      font-size: 13.5px;
      color: var(--color-ink-muted);
      margin-top: 3px;
    }
    .masthead-meta {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .meta-tag {
      font-family: var(--font-mono);
      font-size: 11.5px;
      color: var(--color-ink-muted);
      background: var(--color-surface);
      border: 1px solid var(--color-rule);
      padding: 4px 10px;
      border-radius: var(--radius-sm);
    }
    .meta-tag strong {
      color: var(--color-ink);
    }

    /* Workbench Control Deck */
    .control-deck {
      background: var(--color-surface);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-lg);
      padding: 14px 16px;
      margin-bottom: 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }

    .search-box {
      position: relative;
      flex: 1 1 220px;
      min-width: 190px;
    }
    .search-box input {
      width: 100%;
      background: var(--color-paper);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-md);
      color: var(--color-ink);
      font-family: var(--font-body);
      font-size: 13px;
      padding: 7px 12px 7px 32px;
      outline: none;
      transition: border-color 0.15s;
    }
    .search-box input:focus {
      border-color: var(--color-cobalt);
    }
    .search-icon {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      width: 14px;
      height: 14px;
      color: var(--color-ink-faint);
      pointer-events: none;
    }

    .filter-select {
      background: var(--color-paper);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-md);
      color: var(--color-ink);
      font-family: var(--font-mono);
      font-size: 12px;
      padding: 7px 10px;
      outline: none;
      cursor: pointer;
      transition: border-color 0.15s;
    }
    .filter-select:focus {
      border-color: var(--color-cobalt);
    }

    .btn-top-toggle {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--color-paper);
      border: 1px solid var(--color-rule);
      padding: 7px 12px;
      border-radius: var(--radius-md);
      font-family: var(--font-mono);
      font-size: 12px;
      font-weight: 600;
      color: var(--color-ink-muted);
      cursor: pointer;
      user-select: none;
      transition: all 0.15s;
    }
    .btn-top-toggle:hover {
      border-color: var(--color-ink-faint);
      color: var(--color-ink);
    }
    .btn-top-toggle.active {
      background: var(--color-cobalt-glow);
      border-color: var(--color-cobalt);
      color: var(--color-cobalt);
    }

    .btn-reset {
      background: transparent;
      border: none;
      color: var(--color-ink-faint);
      font-family: var(--font-mono);
      font-size: 11.5px;
      cursor: pointer;
      text-decoration: underline;
      padding: 6px 8px;
    }
    .btn-reset:hover {
      color: var(--color-ink);
    }

    /* Sub-deck Presets Bar */
    .presets-bar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      margin-bottom: 20px;
      font-size: 12px;
      color: var(--color-ink-faint);
    }
    .preset-label {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--color-ink-faint);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .preset-chip {
      background: transparent;
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-sm);
      color: var(--color-ink-muted);
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 3px 9px;
      cursor: pointer;
      transition: all 0.12s;
    }
    .preset-chip:hover {
      border-color: var(--color-cobalt);
      color: var(--color-ink);
    }
    .preset-chip.active {
      background: var(--color-cobalt);
      border-color: var(--color-cobalt);
      color: #fff;
    }

    .counter-line {
      margin-left: auto;
      font-family: var(--font-mono);
      font-size: 12px;
      color: var(--color-ink-muted);
    }
    .counter-line strong {
      color: var(--color-ink);
    }

    /* Grid Layout */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(min(100%, 370px), 1fr));
      gap: 18px;
    }

    /* Debloated Card */
    .card {
      background: var(--color-surface);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-lg);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      transition: border-color 0.15s, transform 0.15s;
    }
    .card:hover {
      border-color: var(--color-ink-faint);
      transform: translateY(-2px);
    }

    .card-photo {
      height: 190px;
      background: #06090e;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      border-bottom: 1px solid var(--color-rule-subtle);
      overflow: hidden;
    }
    .card-photo img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.2s ease;
    }
    .card:hover .card-photo img {
      transform: scale(1.02);
    }

    .tag-grade {
      position: absolute;
      top: 10px;
      left: 10px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.04em;
      z-index: 2;
    }
    .tag-grade.top {
      background: rgba(245, 158, 11, 0.9);
      color: #000;
      border: 1px solid rgba(245, 158, 11, 1);
    }
    .tag-grade.value {
      background: rgba(16, 185, 129, 0.9);
      color: #000;
      border: 1px solid rgba(16, 185, 129, 1);
    }
    .tag-grade.fair {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: var(--color-ink-muted);
    }

    .tag-tier {
      position: absolute;
      top: 10px;
      right: 10px;
      font-family: var(--font-mono);
      font-size: 10.5px;
      padding: 2px 7px;
      border-radius: var(--radius-sm);
      background: rgba(9, 13, 22, 0.88);
      border: 1px solid var(--color-rule);
      color: var(--color-ink-muted);
      z-index: 2;
    }
    .tag-tier.assured {
      color: var(--color-emerald);
      border-color: rgba(16, 185, 129, 0.4);
    }

    .card-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      flex: 1;
    }

    .car-name {
      font-family: var(--font-display);
      font-size: 17px;
      font-weight: 700;
      color: var(--color-ink);
      line-height: 1.25;
    }

    .car-telemetry {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .spec-item {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--color-ink-muted);
      background: var(--color-paper);
      border: 1px solid var(--color-rule);
      padding: 2px 7px;
      border-radius: var(--radius-sm);
    }

    /* Single Clean Metrics Strip */
    .metrics-strip {
      display: grid;
      grid-template-columns: 1fr 1.1fr 1.1fr;
      background: var(--color-paper);
      border: 1px solid var(--color-rule-subtle);
      border-radius: var(--radius-md);
      padding: 8px 12px;
      gap: 8px;
    }
    .metric-col {
      display: flex;
      flex-direction: column;
    }
    .metric-label {
      font-family: var(--font-mono);
      font-size: 9.5px;
      text-transform: uppercase;
      color: var(--color-ink-faint);
      letter-spacing: 0.05em;
    }
    .metric-val {
      font-family: var(--font-mono);
      font-size: 14px;
      font-weight: 700;
      color: var(--color-ink);
      margin-top: 2px;
    }
    .metric-val.monthly {
      color: var(--color-cobalt);
    }
    .metric-val.buyback {
      color: var(--color-emerald);
    }

    /* Crisp One-Line Verdict */
    .car-verdict {
      font-size: 12px;
      color: #cbd5e1;
      line-height: 1.4;
      padding-left: 10px;
      border-left: 2px solid var(--color-cobalt);
    }

    .card-action {
      margin-top: auto;
      padding-top: 8px;
      border-top: 1px solid var(--color-rule-subtle);
    }
    .btn-spinny {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      background: transparent;
      border: 1px solid var(--color-rule);
      color: var(--color-ink-muted);
      font-family: var(--font-mono);
      font-size: 11.5px;
      font-weight: 600;
      padding: 8px 12px;
      border-radius: var(--radius-sm);
      text-decoration: none;
      transition: all 0.15s ease;
    }
    .btn-spinny:hover {
      background: var(--color-cobalt);
      border-color: var(--color-cobalt);
      color: #fff;
    }

    .empty-state {
      grid-column: 1 / -1;
      padding: 60px 20px;
      text-align: center;
      background: var(--color-surface);
      border: 1px dashed var(--color-rule);
      border-radius: var(--radius-lg);
    }
    .empty-state h3 {
      font-family: var(--font-display);
      font-size: 18px;
      margin-bottom: 6px;
    }
    .empty-state p {
      font-size: 13px;
      color: var(--color-ink-muted);
      margin-bottom: 16px;
    }
  </style>
</head>
<body>

  <div class="shell">
    <!-- Masthead -->
    <header class="masthead">
      <div>
        <h1 class="masthead-title">Bangalore Used Cars · Hallmark Screener</h1>
        <p class="masthead-sub">Uncapped Bangalore inventory with 2-year buyback retention and depreciation telemetry.</p>
      </div>
      <div class="masthead-meta">
        <span class="meta-tag">City: <strong>Bangalore</strong></span>
        <span class="meta-tag">Inventory: <strong id="tele-total">0</strong></span>
      </div>
    </header>

    <!-- Debloated Single-Deck Workbench Controls -->
    <div class="control-deck">
      <!-- Search Input -->
      <div class="search-box">
        <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
        </svg>
        <input type="text" id="ctrl-search" placeholder="Search model, hub, variant..." oninput="onSearch(this.value)" />
      </div>

      <!-- Make Year Filter -->
      <select id="ctrl-year" class="filter-select" onchange="onSelectChange('min_year', this.value)">
        <option value="0">Year: All Years</option>
        <option value="2022">2022+ (≤ 4 Yrs)</option>
        <option value="2020">2020+ (≤ 6 Yrs)</option>
        <option value="2018">2018+ (≤ 8 Yrs)</option>
        <option value="2016">2016+ (≤ 10 Yrs)</option>
        <option value="2014">2014+ (≤ 12 Yrs)</option>
      </select>

      <!-- Max Budget (Unrestricted options) -->
      <select id="ctrl-budget" class="filter-select" onchange="onSelectChange('budget', this.value)">
        <option value="0">Budget: Any Price (No Limit)</option>
        <option value="300000">Budget: ≤ ₹3.0 Lakhs</option>
        <option value="400000">Budget: ≤ ₹4.0 Lakhs</option>
        <option value="500000">Budget: ≤ ₹5.0 Lakhs</option>
        <option value="600000">Budget: ≤ ₹6.0 Lakhs</option>
        <option value="800000">Budget: ≤ ₹8.0 Lakhs</option>
        <option value="1000000">Budget: ≤ ₹10.0 Lakhs</option>
        <option value="1500000">Budget: ≤ ₹15.0 Lakhs</option>
        <option value="2000000">Budget: ≤ ₹20.0 Lakhs</option>
      </select>

      <!-- Brand -->
      <select id="ctrl-brand" class="filter-select" onchange="onSelectChange('brand', this.value)">
        <option value="all">Brand: All Brands</option>
        <option value="volkswagen">Volkswagen</option>
        <option value="honda">Honda</option>
        <option value="hyundai">Hyundai</option>
        <option value="maruti">Maruti Suzuki</option>
        <option value="tata">Tata</option>
        <option value="ford">Ford</option>
        <option value="toyota">Toyota</option>
        <option value="skoda">Skoda</option>
        <option value="kia">Kia</option>
        <option value="mahindra">Mahindra</option>
      </select>

      <!-- Gearbox -->
      <select id="ctrl-trans" class="filter-select" onchange="onSelectChange('trans', this.value)">
        <option value="all">Gearbox: All</option>
        <option value="automatic">Automatic Only</option>
        <option value="manual">Manual Only</option>
      </select>

      <!-- Tier -->
      <select id="ctrl-tier" class="filter-select" onchange="onSelectChange('tier', this.value)">
        <option value="all">Tier: All Stock</option>
        <option value="assured">Spinny Assured (Buyback)</option>
        <option value="auction">Wholesale / Budget Stock</option>
      </select>

      <!-- Sort -->
      <select id="ctrl-sort" class="filter-select" onchange="onSelectChange('sort', this.value)">
        <option value="score">Sort: Best Value Score</option>
        <option value="price_asc">Price: Low to High</option>
        <option value="price_desc">Price: High to Low</option>
        <option value="year_desc">Year: Newest First</option>
        <option value="km_asc">Mileage: Lowest KM</option>
      </select>

      <!-- Top Deals Toggle -->
      <button id="btn-top-deals" class="btn-top-toggle" onclick="toggleTopDeals(this)">
        <span>⭐ Top Deals Only</span>
      </button>

      <!-- Clear Filters -->
      <button class="btn-reset" onclick="resetAll()">Reset</button>
    </div>

    <!-- Quick Presets Row -->
    <div class="presets-bar">
      <span class="preset-label">Quick Filters:</span>
      <button class="preset-chip" onclick="applyPreset('polo', this)">Volkswagen Polo</button>
      <button class="preset-chip" onclick="applyPreset('city', this)">Honda City</button>
      <button class="preset-chip" onclick="applyPreset('auto_sub5', this)">Automatic &lt; ₹5L</button>
      <button class="preset-chip" onclick="applyPreset('sub_4l', this)">Under ₹4.0L</button>
      <button class="preset-chip" onclick="applyPreset('low_km', this)">Low KM (&lt; 40k)</button>
      <button class="preset-chip" onclick="applyPreset('assured_only', this)">Spinny Assured</button>

      <div class="counter-line">
        Showing <strong id="res-count">0</strong> vehicles
      </div>
    </div>

    <!-- Cards Grid -->
    <main class="grid" id="cars-grid"></main>
  </div>

  <script>
    const CARS = """ + cars_json + """;

    const state = {
      search: '',
      min_year: 0,
      budget: 0, // 0 means unrestricted
      brand: 'all',
      trans: 'all',
      tier: 'all',
      sort: 'score',
      topDealsOnly: false,
      activePreset: null
    };

    document.getElementById('tele-total').textContent = CARS.length;

    function onSearch(val) {
      state.search = (val || '').toLowerCase().trim();
      applyFilters();
    }

    function onSelectChange(key, val) {
      if (key === 'min_year' || key === 'budget') {
        state[key] = Number(val);
      } else {
        state[key] = val;
      }
      state.activePreset = null;
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));
      applyFilters();
    }

    function toggleTopDeals(btn) {
      state.topDealsOnly = !state.topDealsOnly;
      if (btn) btn.classList.toggle('active', state.topDealsOnly);
      applyFilters();
    }

    function applyPreset(preset, el) {
      state.activePreset = preset;
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));
      if (el) el.classList.add('active');

      // Reset base filters
      state.search = '';
      state.min_year = 0;
      state.budget = 0;
      state.brand = 'all';
      state.trans = 'all';
      state.tier = 'all';
      state.topDealsOnly = false;
      document.getElementById('btn-top-deals').classList.remove('active');

      document.getElementById('ctrl-search').value = '';
      document.getElementById('ctrl-year').value = '0';
      document.getElementById('ctrl-budget').value = '0';
      document.getElementById('ctrl-brand').value = 'all';
      document.getElementById('ctrl-trans').value = 'all';
      document.getElementById('ctrl-tier').value = 'all';

      if (preset === 'polo') {
        state.brand = 'volkswagen';
        state.search = 'polo';
        document.getElementById('ctrl-brand').value = 'volkswagen';
        document.getElementById('ctrl-search').value = 'polo';
      } else if (preset === 'city') {
        state.brand = 'honda';
        state.search = 'city';
        document.getElementById('ctrl-brand').value = 'honda';
        document.getElementById('ctrl-search').value = 'city';
      } else if (preset === 'auto_sub5') {
        state.trans = 'automatic';
        state.budget = 500000;
        document.getElementById('ctrl-trans').value = 'automatic';
        document.getElementById('ctrl-budget').value = '500000';
      } else if (preset === 'sub_4l') {
        state.budget = 400000;
        document.getElementById('ctrl-budget').value = '400000';
      } else if (preset === 'low_km') {
        // Filtered dynamically
      } else if (preset === 'assured_only') {
        state.tier = 'assured';
        document.getElementById('ctrl-tier').value = 'assured';
      }

      applyFilters();
    }

    function resetAll() {
      state.search = '';
      state.min_year = 0;
      state.budget = 0;
      state.brand = 'all';
      state.trans = 'all';
      state.tier = 'all';
      state.sort = 'score';
      state.topDealsOnly = false;
      state.activePreset = null;

      document.getElementById('ctrl-search').value = '';
      document.getElementById('ctrl-year').value = '0';
      document.getElementById('ctrl-budget').value = '0';
      document.getElementById('ctrl-brand').value = 'all';
      document.getElementById('ctrl-trans').value = 'all';
      document.getElementById('ctrl-tier').value = 'all';
      document.getElementById('ctrl-sort').value = 'score';
      document.getElementById('btn-top-deals').classList.remove('active');
      document.querySelectorAll('.preset-chip').forEach(b => b.classList.remove('active'));

      applyFilters();
    }

    function applyFilters() {
      let filtered = CARS.filter(c => {
        if (state.topDealsOnly && !c.is_top_deal) return false;

        if (state.activePreset === 'low_km' && (c.mileage || 0) > 40000) return false;

        if (state.search) {
          const text = `${c.make_year} ${c.make} ${c.model} ${c.variant} ${c.hub} ${c.transmission} ${c.fuel_type}`.toLowerCase();
          if (!text.includes(state.search)) return false;
        }

        if (state.min_year > 0 && (c.make_year || 0) < state.min_year) return false;

        if (state.budget > 0 && (c.price || 0) > state.budget) return false;

        if (state.brand !== 'all') {
          const make = (c.make || '').toLowerCase();
          if (!make.includes(state.brand)) return false;
        }

        if (state.trans !== 'all') {
          const t = (c.transmission || '').toLowerCase();
          const isAuto = t.includes('auto') || t.includes('amt') || t.includes('at') || t.includes('cvt') || t.includes('dsg') || t.includes('dct');
          if (state.trans === 'automatic' && !isAuto) return false;
          if (state.trans === 'manual' && isAuto) return false;
        }

        if (state.tier !== 'all') {
          const tier = (c.category || 'auction').toLowerCase();
          if (tier !== state.tier) return false;
        }

        return true;
      });

      // Sorting
      if (state.sort === 'price_asc') {
        filtered.sort((a, b) => (a.price || 0) - (b.price || 0));
      } else if (state.sort === 'price_desc') {
        filtered.sort((a, b) => (b.price || 0) - (a.price || 0));
      } else if (state.sort === 'year_desc') {
        filtered.sort((a, b) => (b.make_year || 0) - (a.make_year || 0));
      } else if (state.sort === 'km_asc') {
        filtered.sort((a, b) => (a.mileage || 0) - (b.mileage || 0));
      } else {
        // Default: deal_score descending
        filtered.sort((a, b) => (b.deal_score || 0) - (a.deal_score || 0));
      }

      document.getElementById('res-count').textContent = filtered.length;
      render(filtered);
    }

    function render(list) {
      const grid = document.getElementById('cars-grid');
      if (!list.length) {
        grid.innerHTML = `
          <div class="empty-state">
            <h3>No matching vehicles found</h3>
            <p>Try loosening your search filters or resetting to view all Bangalore inventory.</p>
            <button class="filter-select" onclick="resetAll()">Reset All Filters</button>
          </div>
        `;
        return;
      }

      grid.innerHTML = list.map(c => {
        const isAssured = c.category === 'assured';
        const price = '₹' + (c.price / 100000).toFixed(2) + 'L';
        const km = (c.mileage / 1000).toFixed(0) + 'k km';
        const title = `${c.make_year} ${c.make} ${c.model} ${c.variant || ''}`.trim();
        const an = c.analysis || {};
        const buyback = '₹' + ((an.est_buyback_2yr || 0) / 100000).toFixed(2) + 'L';
        const monthly = '₹' + Math.round(an.monthly_loss || 0).toLocaleString('en-IN') + '/mo';

        let gradeClass = 'fair';
        let gradeLabel = `Score ${c.deal_score}`;
        if (c.deal_score >= 80) {
          gradeClass = 'top';
          gradeLabel = `💎 ${c.deal_score} · TOP DEAL`;
        } else if (c.deal_score >= 68) {
          gradeClass = 'value';
          gradeLabel = `⭐ ${c.deal_score} · VALUE PICK`;
        }

        return `
          <article class="card">
            <div class="card-photo">
              <span class="tag-grade ${gradeClass}">${gradeLabel}</span>
              <span class="tag-tier ${isAssured ? 'assured' : ''}">
                ${isAssured ? '✓ Spinny Assured' : '⚡ Wholesale Stock'}
              </span>
              ${c.img ? `<img src="${c.img}" alt="${title}" loading="lazy" />` : '<span style="color:var(--color-ink-faint); font-family:var(--font-mono); font-size:12px;">No Image</span>'}
            </div>
            
            <div class="card-body">
              <div>
                <h2 class="car-name">${title}</h2>
                <div class="car-telemetry" style="margin-top:6px;">
                  <span class="spec-item">${km}</span>
                  <span class="spec-item">${(c.fuel_type || 'Petrol').toUpperCase()}</span>
                  <span class="spec-item">${(c.transmission || 'MT').toUpperCase()}</span>
                  <span class="spec-item" style="color:var(--color-ink-faint);">${c.hub}</span>
                </div>
              </div>

              <!-- Metrics Strip -->
              <div class="metrics-strip">
                <div class="metric-col">
                  <span class="metric-label">Price</span>
                  <span class="metric-val">${price}</span>
                </div>
                <div class="metric-col">
                  <span class="metric-label">${isAssured ? '2-Yr Buyback' : '2-Yr Resale'}</span>
                  <span class="metric-val buyback">${buyback}</span>
                </div>
                <div class="metric-col">
                  <span class="metric-label">Monthly Loss</span>
                  <span class="metric-val monthly">${monthly}</span>
                </div>
              </div>

              <!-- 1-Line Verdict -->
              <p class="car-verdict">${c.verdict || 'Reliable urban commuter with strong parts availability.'}</p>

              <div class="card-action">
                <a href="${c.url || '#'}" target="_blank" rel="noopener noreferrer" class="btn-spinny">
                  <span>Inspect on Spinny</span>
                  <span>&rarr;</span>
                </a>
              </div>
            </div>
          </article>
        `;
      }).join('');
    }

    applyFilters();
  </script>
</body>
</html>
"""

deals_path = os.path.join(DIR, "deals.html")
with open(deals_path, "w") as f:
    f.write(html_content)

# Also sync index.html
index_path = os.path.join(DIR, "index.html")
shutil.copyfile(deals_path, index_path)

print(f"Hallmark debloated UI written to {deals_path} and synced to {index_path}")
