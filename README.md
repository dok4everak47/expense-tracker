# 💰 Expense Tracker

Personal expense tracking app — built from scratch to solve a real problem.

## What It Does

- **Manual entry:** Record daily expenses with amount, category, and notes
- **WeChat import:** Upload exported WeChat bill `.xlsx` files — auto-categorizes 77+ merchants
- **Dashboard:** Monthly KPI cards, category breakdown (doughnut chart), daily spending trend with 7-day average, budget vs actual comparison
- **Budgeting:** Set monthly budgets per category, see over-budget alerts

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13 + FastAPI |
| Database | SQLite |
| Frontend | Vanilla HTML/CSS/JS + ECharts 5.5 |
| Font | Inter |

## Quick Start

```bash
# Install dependencies
uv sync

# Start backend
uv run uvicorn main:app --reload

# Open frontend
open index.html
```

Then visit `http://127.0.0.1:8000/docs` for the interactive API docs.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/expenses` | Add an expense |
| GET | `/expenses` | List expenses (filter by `category`, `date`, `month`) |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |
| GET | `/expenses/summary?month=` | Category breakdown |
| GET | `/expenses/daily?month=` | Daily totals |
| GET | `/expenses/months` | List months with data |
| POST | `/expenses/import` | Upload WeChat `.xlsx` bill |
| GET/POST | `/budget` | Get/set monthly budgets |

## Project Structure

```
├── main.py          # FastAPI backend
├── index.html       # Frontend SPA
├── import_wechat.py # CLI import script (alternative to upload)
├── pyproject.toml   # uv project config
└── .pi/skills/      # Pi AI agent skill (project context)
```

## Background

Built following the framework from [Why Coding Feels Impossible (And How to Fix It)](https://www.youtube.com/watch?v=gaCY4QxfSzA):

> "You are one working prototype away from changing your entire trajectory."
