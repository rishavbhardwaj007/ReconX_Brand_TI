# utils/github.py

import os
import requests

def search_github_leaks(brand):
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("❌ Missing GITHUB_TOKEN")
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    query = f'"{brand}" in:file'
    url = f"https://api.github.com/search/code?q={query}&per_page=5"

    print(f"🔍 Querying GitHub: {url}")
    response = requests.get(url, headers=headers)

    print("📡 GitHub Status Code:", response.status_code)

    if response.status_code != 200:
        print("⚠️ GitHub Response:", response.text)
        return []

    results = []
    data = response.json()

    for item in data.get("items", []):
        repo_name = item.get("repository", {}).get("full_name", "")
        file_path = item.get("path", "")
        file_url = item.get("html_url", "")
        results.append({
            "repo": repo_name,
            "path": file_path,
            "url": file_url
        })
        print(f"✅ Leak found: {repo_name}/{file_path}")

    return results
