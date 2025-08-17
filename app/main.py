from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Optional

# Create one FastAPI app
app = FastAPI(title="Degree Agent v2", version="0.3.0")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Base API (free and open data source)
BASE_URL = "http://universities.hipolabs.com/search"


@app.get("/")
def root():
    return {"message": "Welcome to Degree Agent v2! Use /search?country=India to find universities."}


@app.get("/search")
def search_universities(
    country: str = Query(..., description="Country name, e.g., India, United States"),
    name: Optional[str] = Query(None, description="Filter by university name (optional)")
):
    """Fetches live university data from the public Universities API"""
    params = {"country": country}
    if name:
        params["name"] = name
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data: {e}"}

    data = response.json()

    return {
        "count": len(data),
        "results": data
    }
