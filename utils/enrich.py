# utils/enrich.py

import os
import requests

def shodan_search(brand):
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        return "Shodan API key not set."

    try:
        url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={brand}"
        response = requests.get(url)
        if response.status_code != 200:
            return "Shodan search failed."

        data = response.json()
        matches = data.get("matches", [])
        if not matches:
            return "No exposed devices found on Shodan."

        top_result = matches[0]
        ip = top_result.get("ip_str", "N/A")
        org = top_result.get("org", "N/A")
        port = top_result.get("port", "N/A")
        return f"⚠️ `{brand}` found on Shodan\nIP: `{ip}`\nOrg: `{org}`\nPort: `{port}`"
    except Exception as e:
        return f"Shodan error: {str(e)}"
