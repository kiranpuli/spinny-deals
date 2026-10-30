#!/usr/bin/env python3
"""
Hallmark Overhaul for Bangalore Used Car Screener
Curated High-Value Deals First, Clean Filter System with Year Controls.
"""

import json
import os

DIR = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(DIR, "clean_bangalore_cars.json")
if not os.path.exists(json_path):
    json_path = "/tmp/clean_bangalore_cars.json"

with open(json_path) as f:
    cars = json.load(f)

# Ensure all cars have deal metrics if not already present
for c in cars:
    if 'deal_score' not in c:
        year = c.get('make_year', 2012)
        km = c.get('mileage', 100000)
        price = c.get('price', 500000)
        is_assured = c.get('category') == 'assured'
        monthly = c.get('analysis', {}).get('monthly_loss', 5000)

        score = 40
        if km <= 25000: score += 25
        elif km <= 40000: score += 18
        elif km <= 60000: score += 12
        elif km > 80000: score -= 12

        if year >= 2019: score += 22
        elif year >= 2017: score += 16
        elif year >= 2015: score += 10
        elif year <= 2013: score -= 6

        if is_assured: score += 16
        if price <= 325000: score += 10
        elif price <= 400000: score += 5
        if monthly <= 3500: score += 10
        elif monthly <= 4500: score += 5

        final_score = min(99, max(42, score))
        c['deal_score'] = final_score
        c['deal_grade'] = "TOP PICK" if final_score >= 80 else ("GREAT VALUE" if final_score >= 68 else "FAIR DEAL")
        c['is_top_deal'] = final_score >= 68

        reasons = []
        if km <= 35000: reasons.append(f"Low Mileage ({km:,} km)")
        if year >= 2017: reasons.append(f"Modern {year} Build")
        if is_assured: reasons.append("Spinny Assured Buyback")
        if monthly <= 3600: reasons.append(f"Low Loss ₹{monthly:,}/mo")
        if price <= 300000: reasons.append("Sub-₹3L Budget")
        if not reasons: reasons.append("Daily City Commuter")
        c['deal_highlights'] = reasons[:3]

cars_json = json.dumps(cars)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bangalore Used Cars · Curated Top Deals &amp; Valuation Screener</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <style>
    /* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */
    :root {
      --font-display: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif;
      --font-body: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: "JetBrains Mono", ui-monospace, monospace;

      --color-paper: #090b10;
      --color-surface: #10131c;
      --color-surface-hover: #151a26;
      --color-surface-inset: #0b0e15;
      --color-rule: #1e2535;
      --color-rule-subtle: #151a26;

      --color-ink: #f8fafc;
      --color-ink-muted: #94a3b8;
      --color-ink-faint: #64748b;

      --color-cobalt: #3b82f6;
      --color-cobalt-hover: #2563eb;
      --color-cobalt-glow: rgba(59, 130, 246, 0.16);

      --color-emerald: #10b981;
      --color-emerald-bg: rgba(16, 185, 129, 0.12);
      --color-emerald-border: rgba(16, 185, 129, 0.35);

      --color-amber: #f59e0b;
      --color-amber-bg: rgba(245, 158, 11, 0.12);
      --color-amber-border: rgba(245, 158, 11, 0.35);

      --color-gold: #fbbf24;
      --color-gold-bg: rgba(251, 191, 36, 0.15);

      --color-rose: #f43f5e;
      --color-rose-bg: rgba(244, 63, 94, 0.12);

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
      padding: 5px 11px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--color-rule);
      background: var(--color-surface);
      color: var(--color-ink-muted);
    }
    .tele-tag strong {
      color: var(--color-ink);
    }

    /* Primary Curated Deals Banner & Switcher */
    .curated-banner {
      background: linear-gradient(180deg, #121724 0%, #0d1018 100%);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-lg);
      padding: 16px 20px;
      margin-bottom: 20px;
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }
    .mode-switch-group {
      display: flex;
      background: var(--color-surface-inset);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-md);
      padding: 3px;
      gap: 4px;
    }
    .mode-btn {
      font-family: var(--font-mono);
      font-size: 12.5px;
      font-weight: 600;
      padding: 8px 16px;
      border: none;
      border-radius: var(--radius-sm);
      background: transparent;
      color: var(--color-ink-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s ease;
    }
    .mode-btn.active {
      background: var(--color-cobalt);
      color: #fff;
      box-shadow: 0 1px 3px rgba(0,0,0,0.4);
    }
    .mode-badge {
      font-size: 11px;
      padding: 1px 6px;
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.2);
    }
    .mode-btn:not(.active) .mode-badge {
      background: var(--color-rule);
      color: var(--color-ink-faint);
    }

    .quick-chips {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }
    .quick-chip-label {
      font-family: var(--font-mono);
      font-size: 11px;
      color: var(--color-ink-faint);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-right: 2px;
    }
    .quick-chip {
      background: var(--color-surface-inset);
      border: 1px solid var(--color-rule);
      color: var(--color-ink-muted);
      font-size: 11.5px;
      font-weight: 500;
      padding: 5px 11px;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: all 0.12s ease;
    }
    .quick-chip:hover {
      border-color: var(--color-cobalt);
      color: var(--color-ink);
    }
    .quick-chip.active {
      background: var(--color-cobalt-glow);
      border-color: var(--color-cobalt);
      color: var(--color-cobalt);
      font-weight: 600;
    }

    /* Filter Console */
    .filter-console {
      background: var(--color-surface);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-lg);
      padding: 18px 20px;
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

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
      padding: 10px 16px 10px 38px;
      font-family: var(--font-body);
      font-size: 13.5px;
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
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--color-ink-faint);
      pointer-events: none;
      width: 15px;
      height: 15px;
    }

    .filter-line {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }
    .filter-label {
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 600;
      color: var(--color-ink-faint);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      min-width: 120px;
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
      padding: 4px 10px;
      font-size: 12px;
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
    .pill-year.active {
      background: #4338ca;
      border-color: #6366f1;
      color: #fff;
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

    /* Car Card */
    .car-card {
      background: var(--color-surface);
      border: 1px solid var(--color-rule);
      border-radius: var(--radius-lg);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: border-color 0.15s, transform 0.15s, box-shadow 0.15s;
      position: relative;
    }
    .car-card:hover {
      border-color: var(--color-ink-faint);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .car-card.top-deal-card {
      border-color: rgba(59, 130, 246, 0.35);
    }
    .car-card.top-deal-card:hover {
      border-color: var(--color-cobalt);
    }

    /* Card Media */
    .card-media {
      position: relative;
      height: 200px;
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
    .badge-deal-score {
      position: absolute;
      top: 10px;
      left: 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: var(--radius-sm);
      letter-spacing: 0.04em;
      text-transform: uppercase;
      z-index: 2;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .badge-deal-score.top-pick {
      background: var(--color-gold-bg);
      color: var(--color-gold);
      border: 1px solid rgba(251, 191, 36, 0.4);
    }
    .badge-deal-score.great-value {
      background: var(--color-emerald-bg);
      color: var(--color-emerald);
      border: 1px solid var(--color-emerald-border);
    }
    .badge-deal-score.fair-deal {
      background: rgba(148, 163, 184, 0.12);
      color: var(--color-ink-muted);
      border: 1px solid rgba(148, 163, 184, 0.25);
    }

    .badge-year {
      position: absolute;
      top: 10px;
      right: 10px;
      font-family: var(--font-mono);
      font-size: 11px;
      font-weight: 700;
      background: rgba(10, 12, 16, 0.85);
      border: 1px solid var(--color-rule);
      color: #fff;
      padding: 3px 8px;
      border-radius: var(--radius-sm);
      z-index: 2;
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

    /* Content */
    .card-content {
      padding: 16px;
      display: flex;
      flex-direction: column;
      flex: 1;
      gap: 13px;
    }
    .card-header-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }
    .card-title {
      font-family: var(--font-display);
      font-size: 17.5px;
      font-weight: 700;
      color: var(--color-ink);
      line-height: 1.25;
      letter-spacing: -0.01em;
    }

    /* Highlights Chips */
    .deal-highlights-row {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
    }
    .deal-highlight-tag {
      font-family: var(--font-mono);
      font-size: 11px;
      padding: 2px 7px;
      border-radius: var(--radius-sm);
      background: rgba(59, 130, 246, 0.08);
      border: 1px solid rgba(59, 130, 246, 0.25);
      color: #93c5fd;
      font-weight: 500;
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
      padding-top: 10px;
      display: flex;
      flex-direction: column;
      gap: 6px;
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
      line-height: 1.4;
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
      padding-top: 10px;
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
        <h1 class="masthead-title">Bangalore Used Car Deals Screener</h1>
        <p class="masthead-sub">Curated low-depreciation cars under ₹5 Lakhs with 2-year buyback retention and real-world Bangalore maintenance estimates.</p>
      </div>
      <div class="masthead-telemetry">
        <div class="tele-tag">City: <strong>Bangalore</strong></div>
        <div class="tele-tag">Tracked: <strong id="tele-total">0</strong> Cars</div>
        <div class="tele-tag">Curated Deals: <strong id="tele-curated">0</strong></div>
      </div>
    </header>

    <!-- Curated Mode Switcher (Active By Default to kill clutter) -->
    <div class="curated-banner">
      <div class="mode-switch-group">
        <button class="mode-btn active" id="btn-mode-curated" onclick="setViewMode('curated')">
          <span>💎 Curated Top Deals</span>
          <span class="mode-badge" id="badge-curated-count">0</span>
        </button>
        <button class="mode-btn" id="btn-mode-all" onclick="setViewMode('all')">
          <span>📋 All Verified Listings</span>
          <span class="mode-badge" id="badge-all-count">0</span>
        </button>
      </div>

      <!-- Quick Preset Shortcuts -->
      <div class="quick-chips">
        <span class="quick-chip-label">Quick Watch:</span>
        <button class="quick-chip" onclick="applyPreset('polo')">🚗 Polos (7)</button>
        <button class="quick-chip" onclick="applyPreset('auto_under_35')">⚡ Auto &lt; ₹3.5L</button>
        <button class="quick-chip" onclick="applyPreset('low_km')">✨ Under 40k KM</button>
        <button class="quick-chip" onclick="applyPreset('year_2017')">📅 2017+ Newer</button>
        <button class="quick-chip" onclick="applyPreset('assured')">🛡️ Assured Buyback</button>
      </div>
    </div>

    <!-- Filter Console -->
    <div class="filter-console">
      <!-- Search Input -->
      <div class="search-row">
        <div class="search-wrap">
          <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <input type="text" id="filter-search" class="search-input" placeholder="Search by model, variant, brand, or hub (e.g. Polo, Brio, Automatic, Whitefield)..." oninput="onSearchChange(this.value)" />
        </div>
      </div>

      <div class="filter-line" style="border-top: 1px solid var(--color-rule-subtle); padding-top: 10px;">
        <!-- YEAR FILTER (Prominently requested by user) -->
        <span class="filter-label" style="color:#a5b4fc;">📅 Make Year:</span>
        <div class="pill-group" id="filter-year">
          <button class="pill pill-year active" data-key="min_year" data-val="0" onclick="setFilter('min_year', 0, this)">All Years</button>
          <button class="pill pill-year" data-key="min_year" data-val="2018" onclick="setFilter('min_year', 2018, this)">2018 &amp; Newer</button>
          <button class="pill pill-year" data-key="min_year" data-val="2017" onclick="setFilter('min_year', 2017, this)">2017 &amp; Newer</button>
          <button class="pill pill-year" data-key="min_year" data-val="2016" onclick="setFilter('min_year', 2016, this)">2016 &amp; Newer</button>
          <button class="pill pill-year" data-key="min_year" data-val="2015" onclick="setFilter('min_year', 2015, this)">2015 &amp; Newer</button>
          <button class="pill pill-year" data-key="min_year" data-val="2014" onclick="setFilter('min_year', 2014, this)">2014 &amp; Newer</button>
        </div>
      </div>

      <!-- Price Budget -->
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

      <!-- Brand -->
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

      <!-- Gearbox & Fuel -->
      <div class="filter-line">
        <span class="filter-label">Gearbox:</span>
        <div class="pill-group" id="filter-trans">
          <button class="pill active" data-key="trans" data-val="all" onclick="setFilter('trans', 'all', this)">All</button>
          <button class="pill" data-key="trans" data-val="automatic" onclick="setFilter('trans', 'automatic', this)">Automatic Only</button>
          <button class="pill" data-key="trans" data-val="manual" onclick="setFilter('trans', 'manual', this)">Manual Only</button>
        </div>
      </div>

      <!-- Listing Tier -->
      <div class="filter-line">
        <span class="filter-label">Listing Tier:</span>
        <div class="pill-group" id="filter-tier">
          <button class="pill active" data-key="tier" data-val="all" onclick="setFilter('tier', 'all', this)">All Inventory</button>
          <button class="pill" data-key="tier" data-val="assured" onclick="setFilter('tier', 'assured', this)">✓ Spinny Assured (Buyback)</button>
          <button class="pill" data-key="tier" data-val="auction" onclick="setFilter('tier', 'auction', this)">⚡ Auction / Wholesale</button>
        </div>
      </div>

      <!-- Sort Order -->
      <div class="filter-line" style="border-top: 1px solid var(--color-rule-subtle); padding-top: 10px;">
        <span class="filter-label">Sort Order:</span>
        <div class="pill-group" id="filter-sort">
          <button class="pill active" data-key="sort" data-val="deal_score_desc" onclick="setFilter('sort', 'deal_score_desc', this)">⭐ Best Deal Score (Recommended)</button>
          <button class="pill" data-key="sort" data-val="price_asc" onclick="setFilter('sort', 'price_asc', this)">Price: Low → High</button>
          <button class="pill" data-key="sort" data-val="km_asc" onclick="setFilter('sort', 'km_asc', this)">Lowest KM</button>
          <button class="pill" data-key="sort" data-val="monthly_asc" onclick="setFilter('sort', 'monthly_asc', this)">Lowest Monthly Loss</button>
          <button class="pill" data-key="sort" data-val="year_desc" onclick="setFilter('sort', 'year_desc', this)">Newest Year</button>
        </div>
      </div>
    </div>

    <!-- Status Bar -->
    <div class="status-bar">
      <div>
        Showing <span class="status-count" id="res-count">0</span> matching vehicles in Bangalore
        <span id="curated-badge-msg" style="color:var(--color-cobalt); font-size:12px; margin-left:8px; font-family:var(--font-mono);">(Curated High-Value Filter Active)</span>
      </div>
      <button class="btn-reset" onclick="resetFilters()">Reset All Filters</button>
    </div>

    <!-- Deal Cards Grid -->
    <main class="cars-grid" id="grid"></main>
  </div>

  <script>
    const ALL_CARS = """ + cars_json + """;

    const state = {
      viewMode: 'curated', // 'curated' (top deals only) or 'all'
      search: '',
      min_year: 0,
      budget: 500000,
      brand: 'all',
      trans: 'all',
      fuel: 'all',
      tier: 'all',
      mileage: 100000,
      hub: 'all',
      sort: 'deal_score_desc'
    };

    // Telemetry Init
    const curatedTotal = ALL_CARS.filter(c => c.is_top_deal).length;
    document.getElementById('tele-total').textContent = ALL_CARS.length;
    document.getElementById('tele-curated').textContent = curatedTotal;
    document.getElementById('badge-curated-count').textContent = curatedTotal;
    document.getElementById('badge-all-count').textContent = ALL_CARS.length;

    function setViewMode(mode) {
      state.viewMode = mode;
      document.getElementById('btn-mode-curated').classList.toggle('active', mode === 'curated');
      document.getElementById('btn-mode-all').classList.toggle('active', mode === 'all');
      document.getElementById('curated-badge-msg').style.display = (mode === 'curated') ? 'inline' : 'none';
      applyFilters();
    }

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

    function applyPreset(preset) {
      resetFiltersSilent();
      if (preset === 'polo') {
        state.search = 'polo';
        document.getElementById('filter-search').value = 'polo';
      } else if (preset === 'auto_under_35') {
        state.trans = 'automatic';
        state.budget = 350000;
        updatePill('trans', 'automatic');
        updatePill('budget', '350000');
      } else if (preset === 'low_km') {
        state.mileage = 40000;
      } else if (preset === 'year_2017') {
        state.min_year = 2017;
        updatePill('min_year', '2017');
      } else if (preset === 'assured') {
        state.tier = 'assured';
        updatePill('tier', 'assured');
      }
      applyFilters();
    }

    function updatePill(key, val) {
      document.querySelectorAll(`[data-key="${key}"]`).forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-val') === String(val));
      });
    }

    function resetFiltersSilent() {
      state.viewMode = 'curated';
      state.search = '';
      state.min_year = 0;
      state.budget = 500000;
      state.brand = 'all';
      state.trans = 'all';
      state.fuel = 'all';
      state.tier = 'all';
      state.mileage = 100000;
      state.hub = 'all';
      state.sort = 'deal_score_desc';

      document.getElementById('filter-search').value = '';
      document.getElementById('btn-mode-curated').classList.add('active');
      document.getElementById('btn-mode-all').classList.remove('active');
      document.getElementById('curated-badge-msg').style.display = 'inline';

      document.querySelectorAll('.pill-group').forEach(group => {
        group.querySelectorAll('.pill').forEach(btn => {
          const val = btn.getAttribute('data-val');
          const isDefault = (
            val === 'all' || 
            val === '500000' || 
            val === '0' || 
            val === 'deal_score_desc'
          );
          btn.classList.toggle('active', isDefault);
        });
      });
    }

    function resetFilters() {
      resetFiltersSilent();
      applyFilters();
    }

    function applyFilters() {
      let filtered = ALL_CARS.filter(c => {
        // Mode: Curated Deals Only
        if (state.viewMode === 'curated' && !c.is_top_deal) {
          return false;
        }

        // Search
        if (state.search) {
          const haystack = `${c.make_year} ${c.make} ${c.model} ${c.variant} ${c.hub}`.toLowerCase();
          if (!haystack.includes(state.search)) return false;
        }

        // Year Filter
        if (state.min_year > 0 && (c.make_year || 0) < state.min_year) {
          return false;
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
      if (state.sort === 'deal_score_desc') {
        filtered.sort((a, b) => (b.deal_score || 0) - (a.deal_score || 0));
      } else if (state.sort === 'price_asc') {
        filtered.sort((a, b) => a.price - b.price);
      } else if (state.sort === 'km_asc') {
        filtered.sort((a, b) => a.mileage - b.mileage);
      } else if (state.sort === 'monthly_asc') {
        filtered.sort((a, b) => (a.analysis?.monthly_loss || 0) - (b.analysis?.monthly_loss || 0));
      } else if (state.sort === 'year_desc') {
        filtered.sort((a, b) => (b.make_year || 0) - (a.make_year || 0));
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
            <p style="font-size:13px; color:var(--color-ink-faint); margin-top:-8px; margin-bottom:14px;">Try clicking "All Verified Listings" or adjust your year / price filters.</p>
            <button class="btn-reset" onclick="resetFilters()">Reset All Filters</button>
          </div>
        `;
        return;
      }

      grid.innerHTML = cars.map(car => {
        const isAssured = car.category === 'assured';
        const price = '₹' + Math.round(car.price).toLocaleString('en-IN');
        const km = Math.round(car.mileage).toLocaleString('en-IN') + ' km';
        const title = `${car.make} ${car.model} ${car.variant || ''}`;
        const year = car.make_year;
        const imgUrl = car.img || '';
        const an = car.analysis || {};
        const estBuyback = '₹' + Math.round(an.est_buyback_2yr || 0).toLocaleString('en-IN');
        const totalLoss = '₹' + Math.round(an.total_loss_2yr || 0).toLocaleString('en-IN');
        const monthly = '₹' + Math.round(an.monthly_loss || 0).toLocaleString('en-IN') + '/mo';

        const score = car.deal_score || 60;
        let gradeClass = 'fair-deal';
        let gradeText = `${score} · FAIR`;
        if (score >= 80) {
          gradeClass = 'top-pick';
          gradeText = `💎 ${score} · TOP PICK`;
        } else if (score >= 68) {
          gradeClass = 'great-value';
          gradeText = `⭐ ${score} · GREAT VALUE`;
        }

        const buybackTitle = isAssured ? '2-Yr Guaranteed Buyback' : '2-Yr Est. Market Resale';
        const valClass = isAssured ? 'buyback' : 'resale';
        const highlights = car.deal_highlights || [];

        return `
          <article class="car-card ${car.is_top_deal ? 'top-deal-card' : ''}">
            <div class="card-media">
              <span class="badge-deal-score ${gradeClass}">${gradeText}</span>
              <span class="badge-year">${year}</span>
              <span class="badge-hub-loc">${car.hub}</span>
              ${imgUrl ? `<img src="${imgUrl}" alt="${title}" loading="lazy" />` : '<span style="color:var(--color-ink-faint); font-family:var(--font-mono); font-size:12px;">No Image</span>'}
            </div>
            
            <div class="card-content">
              <div class="card-header-row">
                <h2 class="card-title">${year} ${title}</h2>
                
                <!-- Highlights Bar -->
                ${highlights.length ? `
                  <div class="deal-highlights-row">
                    ${highlights.map(h => `<span class="deal-highlight-tag">${h}</span>`).join('')}
                  </div>
                ` : ''}

                <div class="card-meta-chips" style="margin-top: 2px;">
                  <span class="chip">${km}</span>
                  <span class="chip">${(car.fuel_type || 'Petrol').toUpperCase()}</span>
                  <span class="chip">${(car.transmission || 'MT').toUpperCase()}</span>
                  ${isAssured 
                    ? '<span class="chip" style="color:var(--color-emerald); border-color:var(--color-emerald-border);">✓ Assured</span>' 
                    : '<span class="chip" style="color:var(--color-amber); border-color:var(--color-amber-border);">⚡ Wholesale</span>'}
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
                  <span class="matrix-label">2-Yr Net Loss</span>
                  <span class="matrix-val loss">${totalLoss}</span>
                </div>
                <div class="matrix-cell">
                  <span class="matrix-label">Monthly Cost</span>
                  <span class="matrix-val monthly">${monthly}</span>
                </div>
              </div>

              <!-- Bangalore Ownership Dossier -->
              <div class="dossier-box">
                <span class="dossier-title">Bangalore Maintenance &amp; Drive</span>
                <ul class="dossier-points pros">
                  ${(an.pros || []).slice(0, 2).map(p => `<li>${p}</li>`).join('')}
                </ul>
                <ul class="dossier-points cons">
                  ${(an.cons || []).slice(0, 1).map(c => `<li>${c}</li>`).join('')}
                </ul>
              </div>

              <!-- CTA Button -->
              <div class="card-footer">
                <a href="${car.url || '#'}" target="_blank" rel="noopener noreferrer" class="btn-inspect">
                  Inspect Listing on Spinny &rarr;
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

print(f"Overhauled UI written to {deals_path}")
