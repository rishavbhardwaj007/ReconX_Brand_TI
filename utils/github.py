import requests
import os

def search_github_leaks(brand):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN is missing")
        return []

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.text-match+json"
    }

    query = f'"{brand}" in:file'
    url = f"https://api.github.com/search/code?q={query}&per_page=10"

    print(f"🔍 GitHub Search URL: {url}")
    response = requests.get(url, headers=headers)
    print(f"📡 GitHub status: {response.status_code}")

    if response.status_code != 200:
        print("⚠️ GitHub error:", response.text)
        return []

    data = response.json()
    results = []

    for item in data.get("items", []):
        print("✅ Found:", item["html_url"])
        results.append({
            "repo": item["repository"]["full_name"],
            "path": item["path"],
            "url": item["html_url"]
        })

    return results
