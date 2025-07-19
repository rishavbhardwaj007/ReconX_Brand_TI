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
        return [f"GitHub API error: {response.status_code} - {response.text}"]

    data = response.json()
    results = []

    for item in data.get("items", []):
        repo = item["repository"]["full_name"]
        file_path = item["path"]
        html_url = item["html_url"]
        results.append(f"Repo: {repo}, File: {file_path}, Link: {html_url}")

    return results or ["No results found."]
