import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Optional

# Import our new functions
from cache_manager import load_cache, save_cache
from scorecard_api import search_colleges

# Load environment variables for the API key
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Degree Agent v2", version="1.1.0") # Version updated

# --- CORS Configuration ---
origins = [
    "https://degree-agent.vercel.app",
    "https://degree-agent-suhail-majeed-s-projects.vercel.app",
]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    return {"status": "ok"}

# === Basic Search (Hipolabs API with Cache) ===
HIPOLABS_BASE_URL = "http://universities.hipolabs.com/search"

@app.get("/")
def root():
    return {"message": "Welcome to Degree Agent v2!"}

@app.get("/search")
def search_universities(
    country: str = Query(..., description="Country name, e.g., India"),
    name: Optional[str] = Query(None, description="University name")
):
    cached_data = load_cache(country)
    if cached_data:
        if name:
            filtered_results = [u for u in cached_data if name.lower() in u.get("name", "").lower()]
            return {"count": len(filtered_results), "results": filtered_results, "source": "cache"}
        return {"count": len(cached_data), "results": cached_data, "source": "cache"}

    print(f"No fresh cache for {country}. Fetching from API.")
    params = {"country": country}
    try:
        response = requests.get(HIPOLABS_BASE_URL, params=params, timeout=60)
        response.raise_for_status()
        api_data = response.json()
        save_cache(country, api_data)
        if name:
            filtered_results = [u for u in api_data if name.lower() in u.get("name", "").lower()]
            return {"count": len(filtered_results), "results": filtered_results, "source": "api"}
        return {"count": len(api_data), "results": api_data, "source": "api"}
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch data from Hipolabs API: {str(e)}"}

# === Advanced Search (U.S. College Scorecard API) ===
@app.get("/advanced-search-us")
def advanced_search_us_colleges(
    school_name: Optional[str] = Query(None, description="Name of the U.S. school"),
    major: Optional[str] = Query(None, description="Major or program of study (simplified search)")
):
    """
    Performs an advanced search for U.S. colleges using the College Scorecard API.
    """
    # Securely get the API key from the environment
    api_key = os.getenv("COLLEGE_SCORECARD_API_KEY")
    if not api_key:
        return {"error": "API key is not configured on the server."}

    results = search_colleges(api_key=api_key, school_name=school_name, major=major)
    return {"count": len(results), "results": results, "source": "collegescorecard"}
