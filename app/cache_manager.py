import json
import os
from datetime import datetime, timedelta

# Define the directory where we will store our cache files
CACHE_DIR = "cache"
# Set how long the cache is valid for (24 hours)
CACHE_DURATION = timedelta(hours=24)

# Ensure the cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_filepath(country: str) -> str:
    """Generates a safe filename for the country's cache file."""
    # Sanitize the country name to create a valid filename
    safe_filename = "".join(c for c in country if c.isalnum()).lower()
    return os.path.join(CACHE_DIR, f"{safe_filename}.json")

def load_cache(country: str) -> dict | None:
    """
    Tries to load data from a cache file for a given country.
    Returns the data if the cache is fresh, otherwise returns None.
    """
    filepath = get_cache_filepath(country)
    
    if not os.path.exists(filepath):
        # The file doesn't exist, so there's no cache
        return None
        
    try:
        # Check how old the file is
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
        if datetime.now() - file_mod_time > CACHE_DURATION:
            # The cache is older than 24 hours, so it's stale
            print(f"Cache for {country} is stale.")
            return None
            
        # If we get here, the cache is fresh. Let's load and return it.
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f"Loading fresh cache for {country}.")
            return json.load(f)
            
    except (IOError, json.JSONDecodeError) as e:
        # If there's any error reading the file, treat it as no cache
        print(f"Error reading cache file for {country}: {e}")
        return None

def save_cache(country: str, data: dict):
    """Saves the university data for a country to a cache file."""
    filepath = get_cache_filepath(country)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            # Write the data to the file in a human-readable format
            json.dump(data, f, indent=4)
            print(f"Successfully saved cache for {country}.")
    except IOError as e:
        print(f"Error saving cache file for {country}: {e}")

