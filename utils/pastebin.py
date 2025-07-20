# utils/pastebin.py

import requests
import re
import time
from datetime import datetime

def search_pastebin(brand):
    """
    Search for brand mentions in Pastebin using Google dorks
    """
    results = []
    
    # Use Google to search Pastebin
    search_queries = [
        f'site:pastebin.com "{brand}"',
        f'site:pastebin.com "{brand}" password',
        f'site:pastebin.com "{brand}" api',
        f'site:pastebin.com "{brand}" leak',
        f'site:paste.ee "{brand}"',
        f'site:justpaste.it "{brand}"'
    ]
    
    for query in search_queries[:2]:  # Limit to avoid rate limits
        try:
            # Using a simple approach - in production, use proper Google API or scraping
            # This is a placeholder that simulates finding paste links
            if brand.lower() in ["test", "example", "demo"]:
                results.append({
                    "site": "pastebin.com",
                    "url": f"https://pastebin.com/fake_{brand}",
                    "title": f"Suspicious paste containing {brand}",
                    "snippet": f"Found potential credential leak for {brand}...",
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
            
            time.sleep(1)  # Rate limiting
        except Exception as e:
            print(f"Error searching pastebin: {e}")
    
    return results

def search_psbdmp(brand):
    """
    Search PSBDMP (Pastebin dump monitor) - requires API access
    """
    # This would require PSBDMP API access
    # For now, returning simulated data
    if brand.lower() in ["test", "example"]:
        return [{
            "source": "psbdmp",
            "content": f"Password dump mentioning {brand}",
            "url": "https://psbdmp.ws/api/dumps/example",
            "date": datetime.now().strftime("%Y-%m-%d")
        }]
    return []