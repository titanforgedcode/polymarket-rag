# fetch_markets.py
import requests
import json

def fetch_polymarket_markets():
    """Fetch markets from Polymarket API"""
    
    url = "https://gamma-api.polymarket.com/markets"
    
    print(f"Fetching from: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status code: {response.status_code}")
        
        response.raise_for_status()
        
        markets = response.json()
        print(f"Response type: {type(markets)}")
        print(f"Number of markets: {len(markets) if isinstance(markets, list) else 'Not a list'}")
        
        if not markets:
            print("No markets returned!")
            return None
            
        # Print first 5 markets
        for i, market in enumerate(markets[:3], 1):

            volume = market.get('volume', '0')

            #DEBUG: Showing Volume Values To Double Check
            #print(f"Volume {i} volume: ${volume}")
            if float(volume) < 10000:
                continue

            print(f"\n{i}. {market.get('question', 'No question')}")
            print(f"   Category: {market.get('category', 'Unknown')}")
            print(f"   Active: {market.get('active', False)}")
            print(f"   Volume: ${volume}")
        
        return markets
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching markets: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response text: {response.text[:500]}")
        return None

if __name__ == "__main__":
    print("Starting market fetch...\n")
    markets = fetch_polymarket_markets()
    
    if markets:
        with open('markets_data.json', 'w') as f:
            json.dump(markets[:10], f, indent=2)
        print("\n✓ Saved first 10 markets to markets_data.json")
    else:
        print("\n✗ Failed to fetch markets")