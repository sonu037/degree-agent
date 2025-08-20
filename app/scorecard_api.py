import requests
from typing import List, Dict, Any, Optional

# The base URL for the College Scorecard API
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools.json"

def search_colleges(
    api_key: str,
    school_name: Optional[str] = None,
    major: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Searches for U.S. colleges using the College Scorecard API.
    """
    if not api_key:
        print("API Key is missing.")
        return []

    params = {
        "api_key": api_key,
        "fields": "id,school.name,school.city,school.state,latest.student.size,latest.cost.tuition.in_state",
        "per_page": 50  # Limit to 50 results per search for now
    }
    
    # Add filters to the query if they are provided
    filters = []
    if school_name:
        filters.append(f"school.name__iword={school_name}")
    if major:
        # This is a simplified search. A real implementation would map majors to specific program codes.
        # For now, we search for the major keyword in the program list.
        # Note: This is a pseudo-filter as the API doesn't directly support full-text search on majors this way.
        # A more advanced implementation would fetch all schools and then filter, or use specific program codes.
        # For our purpose, we'll simulate this by searching the school name for now.
        # This part highlights the complexity of real-world API integration.
        # To keep this step manageable, we will filter by school name instead of major for now.
        # In Phase 3, we would build a proper major-to-code mapping.
        pass # Placeholder for more advanced major filtering

    # The API uses a 'school.operating' flag to find currently open schools.
    params["school.operating"] = "true"

    if school_name: # Simplified search for this phase
         params["school.name"] = school_name

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # The actual school data is in the 'results' key
        return data.get("results", [])

    except requests.exceptions.RequestException as e:
        print(f"An error occurred calling College Scorecard API: {e}")
        return []

