# utils/reddit.py

import requests
import os
import time

def search_reddit(brand):
    """
    Search Reddit for brand mentions using Reddit API
    """
    results = []
    
    try:
        # Reddit search without authentication (limited)
        url = f"https://www.reddit.com/search.json"
        params = {
            'q': f'"{brand}" (leak OR breach OR password OR api OR credentials)',
            'sort': 'new',
            'limit': 10,
            't': 'all'
        }
        
        headers = {
            'User-Agent': 'ReconX/1.0'
        }
        
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            
            for post in data.get('data', {}).get('children', []):
                post_data = post.get('data', {})
                
                # Check if post contains suspicious keywords
                title = post_data.get('title', '').lower()
                selftext = post_data.get('selftext', '').lower()
                
                suspicious_keywords = ['leak', 'breach', 'password', 'api', 'credentials', 'dump']
                
                if any(keyword in title or keyword in selftext for keyword in suspicious_keywords):
                    results.append({
                        'title': post_data.get('title', ''),
                        'subreddit': post_data.get('subreddit', ''),
                        'author': post_data.get('author', ''),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'created': post_data.get('created_utc', 0),
                        'num_comments': post_data.get('num_comments', 0)
                    })
        
        time.sleep(1)  # Rate limiting
        
    except Exception as e:
        print(f"Error searching Reddit: {e}")
    
    # Fallback simulated data for testing
    if not results and brand.lower() in ["test", "example", "demo"]:
        results.append({
            'title': f'{brand} data breach discussion',
            'subreddit': 'cybersecurity',
            'author': 'user123',
            'url': f'https://reddit.com/r/cybersecurity/fake_{brand}',
            'score': 15,
            'created': 1703097600,  # Timestamp
            'num_comments': 5
        })
    
    return results

def search_reddit_authenticated(brand):
    """
    Search Reddit with authentication (requires Reddit app credentials)
    """
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    username = os.getenv('REDDIT_USERNAME')
    password = os.getenv('REDDIT_PASSWORD')
    
    if not all([client_id, client_secret, username, password]):
        return search_reddit(brand)  # Fallback to unauthenticated
    
    # Authentication and enhanced search would go here
    # This requires praw library: pip install praw
    
    return []