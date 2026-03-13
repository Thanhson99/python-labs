from serpapi import GoogleSearch
import os

API_KEY = os.getenv("SERPAPI_API_KEY", "your_serpapi_api_key")
SEARCH_QUERIES = [
    "sorting algorithm Python implementation site:geeksforgeeks.org",
    "sorting algorithm Java example site:geeksforgeeks.org",
    "sorting algorithm C++ code site:github.com",
    "sorting algorithm site:stackoverflow.com"
]

def search_algorithms():
    urls = []
    for query in SEARCH_QUERIES:
        params = {
            "q": query,
            "api_key": API_KEY,
            "engine": "google",
            "num": 5  # Limit to 5 results per source
        }
        search = GoogleSearch(params)
        results = search.get_dict()

        for result in results.get("organic_results", []):
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            if any(kw in title or kw in snippet for kw in ["code", "example", "implementation"]):
                urls.append(result["link"]) 

    return urls
