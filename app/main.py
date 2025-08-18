from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Optional

# Create one FastAPI app
app = FastAPI(title="Degree Agent v2", version="0.5.0") # Version updated

# --- FINAL FIX: Update CORS to allow your specific Vercel domains ---
origins = [
    "https://degree-agent.vercel.app",
    "https://degree-agent-suhail-majeed-s-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# --- NEW: Add a Health Check endpoint for Render ---
@app.get("/health")
def health_check():
    """A simple endpoint to confirm the API is running."""
    return {"status": "ok"}

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
        # Increased timeout to 60 seconds to handle server cold starts.
        response = requests.get(BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()

        return {
            "count": len(data),
            "results": data
        }

    except requests.exceptions.Timeout:
        return {"error": "The university API took too long to respond. This can happen during a server cold start. Please try again in a moment."}

    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data from the university API: {str(e)}"}
