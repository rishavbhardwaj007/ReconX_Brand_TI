# utils/github.py

import requests
import os

def search_github_leaks(brand):
    token = os.getenv("GITHUB_TOKEN")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.text-match+json"
    }

    query = f'"{brand}" in:file'
    url = f"https://api.github.com/search/code?q={query}&per_page=5"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for item in data.get("items", []):
        results.append({
            "repo": item["repository"]["full_name"],
            "path": item["path"],
            "url": item["html_url"]
        })

    return results

