# 🚗 Spinny Bangalore Prestige Deals & 2-Year Buyback Tracker

> **Live Web App**: [https://kiranpuli.github.io/spinny-deals/](https://kiranpuli.github.io/spinny-deals/)

An automated tracker and interactive dashboard for high-retention, prestigious used cars in **Bangalore** listed on Spinny, strictly under **₹5 Lakhs**, backed by **Spinny Assured Guaranteed Buyback**.

Built for drivers looking to own a dependable, prestigious car for **1.5 to 2 years** and return it for an assured price with minimal monthly depreciation.

---

## 🎯 Key Highlights

- **Strict Budget Ceiling**: Hard capped at &le; ₹5,00,000 (currently tracking top options from ₹3.01L).
- **Brand Prestige Filter**: Whitelists high-resale brands (**Honda, Volkswagen, Skoda, Toyota**, and premium trims of **Hyundai, Ford, Maruti**); excludes budget fleet cars (*Alto, Eeco, Omni, Santro, Kwid, S-Presso*).
- **Guaranteed Buyback Eligibility**: Only tracks `Spinny Assured` & `Spinny Assured Plus` verified inventory.
- **2-Year Financial Depreciation Modeling**:
  - Estimated 2-Year Buyback / Resale Value
  - Net 2-Year Loss Calculation
  - Effective Monthly Ownership Cost (often &le; ₹3,500 – ₹4,800/mo)
  - Annual Bangalore Servicing & Maintenance Estimates
- **Real-World Bangalore Insights**: Highlights daily traffic drivability, pothole suspension handling, and local spare parts availability for each model.
- **Zero-Touch Cloud Cron**: Automated GitHub Actions workflow crawls the internal Spinny API every morning at **8:30 AM IST** and redeploys to GitHub Pages automatically.

---

## 📊 Live Interactive Dashboard

The dashboard provides instant, client-side filtering without page reloads:

| Filter | Options |
|---|---|
| **Max Budget** | &le; ₹3.5 Lakhs &bull; &le; ₹4.0 Lakhs &bull; &le; ₹4.5 Lakhs &bull; &le; ₹5.0 Lakhs |
| **Brand** | All &bull; Honda &bull; Hyundai &bull; Ford &bull; Volkswagen &bull; Skoda &bull; Maruti |
| **Transmission** | All &bull; Automatic Only &bull; Manual Only |
| **Sort By** | Cheapest First &bull; Lowest Mileage &bull; Lowest Monthly Loss |

Each card provides direct click-through access via the **"View on Spinny &rarr;"** button.

---

## 🛠️ Architecture & Pipeline

```
GitHub Actions Cron (8:30 AM IST Daily)
   │
   ▼
spinny_checker.py (Crawls Spinny v7 API + Enriches Metrics)
   │
   ▼
build_ui.py (Compiles Static Single-Page HTML)
   │
   ▼
index.html / deals.html (Pushed to main branch)
   │
   ▼
GitHub Pages (Live Deployment at kiranpuli.github.io/spinny-deals/)
```

---

## 💻 Local Setup & Execution

### 1. Run Deal Checker
```bash
python3 spinny_checker.py --city bangalore --max-price 500000
```

### 2. Open Local Dashboard
```bash
open deals.html
```

### 3. Run Local Interactive Server
```bash
python3 server.py
# Open http://localhost:8080
```
