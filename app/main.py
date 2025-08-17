from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Optional

# Create one FastAPI app
app = FastAPI(title="Degree Agent v2", version="0.3.0")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For now allow all origins, later restrict to Vercel domain
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
        # Add a timeout to avoid hanging forever
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        return {
            "count": len(data),
            "results": data
        }

    except requests.exceptions.Timeout:
        return {"error": "Hippo Labs API took too long to respond. Please try again."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data from Hippo Labs: {str(e)}"}
