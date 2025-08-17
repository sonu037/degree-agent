# Degree Agent v2 — Find Free/Low-Cost Online Degrees (MVP)

This is a ready-to-run Python project for an AI agent that helps students discover **online, credible, and free/low-cost** university programs.  
It ships with a small **seed dataset** and a **FastAPI** endpoint so you can test instantly in VS Code.

## Quick Start
1. **Install Python 3.9+**
2. Open this folder in **VS Code**.
3. In a terminal:
   ```bash
   python -m venv .venv && . .venv/bin/activate  # (Windows: .venv\Scripts\activate)
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
4. Open the docs at: http://127.0.0.1:8000/docs

## Sample Queries
- `/search?discipline=AI&tuition_type=tuition_free`
- `/search?max_total_fees=5000&modality=Online`
- `/search?q=computer science&degree_level=Masters`

## Project Structure
```
app/
  main.py          - FastAPI API
  schemas.py       - Pydantic models
  search.py        - Scoring + filters
  sources/         - Source stubs (for future crawling)
  data/seed_programs.json
scripts/
  crawl_stub.py    - Where real crawlers will live
tests/
  test_api.py
README.md
requirements.txt
```

## Roadmap
- Add real crawlers in `scripts/crawl_stub.py` (Requests/BS4/Playwright)
- Save programs to a DB (SQLite/Postgres)
- Add scholarships/fee breakdown enrichment
- Add vector search (semantic) and re-ranking
- Build a React/Next.js UI front-end
