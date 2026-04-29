# AI Room Designer — Global Sourcing Cost Analyzer

Upload a room photo. Get AI-powered furniture recommendations with estimated global sourcing costs.

## What it does

1. Upload a room photo
2. Claude AI detects the room style and identifies missing items
3. Matching products are pulled from a furniture catalog
4. Each product shows: origin country, HS code, duty rate, freight estimate, and total landed cost

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
cp ../.env.example .env   # add your ANTHROPIC_API_KEY
uvicorn main:app --reload
```

API runs at `http://localhost:8000`. Swagger docs at `http://localhost:8000/docs`.

### Frontend

Open `frontend/index.html` directly in your browser. No build step needed.

## Project structure

```
room-designer/
├── backend/
│   ├── main.py        FastAPI endpoint: POST /analyze-room
│   ├── vision.py      Claude vision API — detects room style + missing items
│   ├── catalog.py     Mock furniture catalog (30 products, 6 styles)
│   ├── sourcing.py    Landed cost calculator (duty + freight)
│   └── requirements.txt
├── frontend/
│   ├── index.html     Upload UI + results page
│   ├── app.js         Fetch, render, DOM logic
│   └── style.css      Card layout and styles
└── .env               Your API key (gitignored — never commit this)
```

## Built with

- [Claude API](https://www.anthropic.com) — vision analysis
- [FastAPI](https://fastapi.tiangolo.com) — backend
- Vanilla HTML/JS — frontend
