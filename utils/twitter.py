# ✅ FILE: utils/twitter.py

import requests
from bs4 import BeautifulSoup

def search_twitter(brand):
    return search_nitter(brand)

def search_nitter(brand):
    results = []
    nitter_instances = [
        'https://nitter.net',
        'https://nitter.privacydev.net',
        'https://nitter.poast.org'
    ]

    for instance in nitter_instances:
        try:
            url = f"{instance}/search?f=tweets&q={brand}%20(leak%20OR%20breach%20OR%20password)"
            headers = {'User-Agent': 'ReconX/1.0'}

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            tweets = soup.find_all('div', class_='timeline-item')

            for tweet in tweets[:5]:
                text = tweet.find('div', class_='tweet-content').text.strip()
                date = tweet.find('span', class_='tweet-date').text.strip()
                url = f"{instance}{tweet.find('a', class_='tweet-link')['href']}"

                results.append({
                    'text': text,
                    'created_at': date,
                    'url': url,
                    'author_id': 'nitter'
                })
            break  # Use only one successful instance
        except Exception as e:
            continue

    return results
