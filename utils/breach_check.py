# ✅ FILE: utils/breach_check.py

import requests
import time

def check_haveibeenpwned(brand):
    results = []

    try:
        url = f"https://api.leak-lookup.com/?key=1bf94ff907f68d511de9a610a6ff9263&type=email&check=admin@{brand}"
        headers = {'User-Agent': 'ReconX-Scanner'}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("found"):
                results.append({
                    'name': f"{brand} Exposure",
                    'title': f"Leak-lookup found credentials",
                    'domain': brand,
                    'breach_date': 'Unknown',
                    'added_date': time.strftime("%Y-%m-%d"),
                    'pwn_count': data.get("found"),
                    'description': f"Leak-lookup returned {data.get('found')} entries for {brand}",
                    'data_classes': ["Emails", "Passwords"]
                })
    except Exception as e:
        print(f"Leak-lookup error: {e}")

    return {
        'breaches': results,
        'pastes': []
    }
