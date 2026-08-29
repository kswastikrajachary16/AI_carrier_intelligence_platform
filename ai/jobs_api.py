import requests
from config import RAPIDAPI_KEY

URL = "https://jsearch.p.rapidapi.com/search-v2"


def search_jobs(
    query,
    country="in",
    page=1,
    date_posted="all"
):

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "jsearch.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    params = {
        "query": query,
        "page": str(page),
        "num_pages": "1",
        "country": country,
        "date_posted": date_posted
    }

    response = requests.get(
        URL,
        headers=headers,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    # IMPORTANT
    
    return data.get("data", {}).get("jobs", [])