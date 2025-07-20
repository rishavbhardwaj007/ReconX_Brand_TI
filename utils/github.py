import requests
import os

def search_github_leaks(brand):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN not found in environment!")
        return []

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.text-match+json"
    }

    query = f'"{brand}" in:file'
    url = f"https://api.github.com/search/code?q={query}&per_page=30"
    print(f"📡 Searching GitHub for: {brand}")

    response = requests.get(url, headers=headers)
    print(f"🔄 GitHub API status: {response.status_code}")

    if response.status_code != 200:
        print(f"⚠️ GitHub error: {response.text}")
        return []

    data = response.json()
    results = []

    for item in data.get("items", []):
        results.append({
            "repo": item["repository"]["full_name"],
            "path": item["path"],
            "url": item["html_url"]
        })

    print(f"✅ GitHub results found: {len(results)}")
    return results
