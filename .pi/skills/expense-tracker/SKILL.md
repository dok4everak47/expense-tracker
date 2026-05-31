---
name: expense-tracker
description: Personal expense tracking app built with Python FastAPI + SQLite backend and vanilla HTML/JS frontend with ECharts. Use when working on this project for any changes, debugging, or feature additions.
---

# Expense Tracker

## Quick Start

```bash
cd /Users/dok4ever/expense-tracker
uv run uvicorn main:app --reload
open index.html
```

## Tech Stack

- **Backend:** Python 3.13 + FastAPI + SQLite
- **Frontend:** Vanilla HTML/JS + ECharts 5.5 (CDN)
- **Font:** Inter (Google Fonts)
- **Package Manager:** uv (with .venv)

## Database

- `expenses.db` - SQLite database with two tables:
  - `expenses` (id, amount, category, note, date)
  - `budgets` (id, category, amount, month, UNIQUE on category+month)
- 30 days of real WeChat expense data imported (May 2026)

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/expenses` | Add expense (amount, category, note, date) |
| GET | `/expenses?category=&date=&month=` | List expenses with optional filters |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |
| GET | `/expenses/summary?month=` | Category summary with totals |
| GET | `/expenses/daily?month=` | Daily spending totals |
| GET | `/expenses/months` | List all months with data |
| POST | `/expenses/import` | Upload WeChat .xlsx bill file |
| GET | `/budget?month=` | Get budget settings for a month |
| POST | `/budget` | Set budget settings (month, budgets dict) |

## Frontend Pages

- **记账 (Journal):** Two-column layout - form + summary on left, filterable expense list on right
- **报表 (Report):** KPI cards, ECharts doughnut chart (category breakdown), daily bar chart with 7-day moving average, budget comparison grouped bar chart. Click chart bars to open detail modals.
- **预算 (Budget):** Set monthly budget per category
- **导入 (Import):** Upload WeChat .xlsx bill files with smart categorization

## Key Implementation Details

- CORS enabled for all origins
- Smart category mapping from WeChat merchant names (see CATEGORY_MAP in main.py)
- Budget comparison: grouped bars (actual colored, budget yellow with orange border)
- Daily chart: indigo bars (#818cf8) + red 7-day average line
- ECharts instances cached on DOM elements (`_echart` property)
- Tab state persisted in localStorage
- Chart click events trigger detail modals

## Files

- `main.py` - FastAPI backend with all endpoints
- `index.html` - Complete frontend (SPA with tab navigation)
- `import_wechat.py` - Standalone CLI import script (alternative to upload)
- `expenses.db` - SQLite database
- `.venv/` - uv virtual environment
- `.pi/skills/expense-tracker/SKILL.md` - This file

## Future Ideas

- Push to GitHub
- Month-over-month comparison
- CSV export
- Weekly statistics view

---

## Background: The YouTube Video That Inspired This Project

**Why Coding Feels Impossible (And How to Fix It)**
https://www.youtube.com/watch?v=gaCY4QxfSzA

### Core Thesis
Tech doesn't reward "knowers" — it rewards "solvers." Most beginners fail not because they lack intelligence, but because their learning model is fundamentally broken.

### The Framework (10 Steps)
1. **Pick one customer** — one person with one painful problem (in this case: yourself, tracking expenses)
2. **Define your ideal user** — what are they duct-taping with Google Sheets right now?
3. **Pick one stack** — lock it in for 60-90 days. No wander. (Python + FastAPI + SQLite)
4. **Rule of 100** — 100 min/day coding actual app, 100 lines/day, 100 outreach messages/month
5. **Build core loop first** — login → action → result. That's it. No dessert before protein.
6. **Post it publicly** — ugly screenshots, 30-sec captures. Attracts testers and feedback.
7. **Builder environment** — mentorship, code review, peers who ask "Is it live yet?"
8. **Kill your ego** — trash code, waste days, feel like you went backwards. That's growth.
9. **Repeat until someone says** "Hey, can I use that?" — worth more than any certificate.
10. **Fork in the road** — Option A: keep waiting/collecting playlists. Option B: pick one user, one stack, one problem, start building today.

### Key Business Analogies
- **LTV (Lifetime Value):** Your ability to earn, build products, launch startups
- **CAC (Acquisition Cost):** Time/frustration spent learning the wrong way
- **Payback Period:** If you only consume, it approaches infinity → burnout

### Key Quotes
- "AI writes code you don't understand → you own nothing. That's dependency with lipstick."
- "School is built for grades. Industry is built for shipping. Different game."
- "Waiting is the new quitting."
- "You are one working prototype away from changing your entire trajectory."

### Anti-Patterns to Avoid
- Stack hopping ("I'll learn JS and Python and Rust and React...")
- Tutorial hell (consuming without shipping)
- AI as boss instead of assistant ("Build me a dashboard" without understanding)
- Learning alone with zero accountability
- Chasing "job-ready" without becoming "project-ready"
