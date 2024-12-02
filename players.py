import requests
import json
import time
from main import REGIONS, API_KEY, OUTPUT_PATH_ROOT, RATE_LIMIT_CALLS, RATE_LIMIT_WINDOW

# Fetch top players from a region
def fetch_top_players(region):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()['entries']
        for player in data:
            player['region'] = region  
        return data
    else:
        print(f"Error: Cannot get players from {region}. Status code: {response.status_code}")
        return []

# Fetch player's puuid with rate limit handling
def fetch_puuid_with_rate_limit(summonerId, region):
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}?api_key={API_KEY}"
    
    while True:
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json().get('puuid')
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))
            print(f"Rate limit reached. Pausing for {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"Error {response.status_code} for summonerId {summonerId}")
            return None

# Main function to collect player data
def collect_players_data():
    all_players_data = []

    for region in REGIONS:
        print(f"Collecting players from region: {region}")
        players = fetch_top_players(region)
        
        for index, player in enumerate(players):
            player['puuid'] = fetch_puuid_with_rate_limit(player['summonerId'], region)
            all_players_data.append(player)
            
            if (index + 1) % RATE_LIMIT_CALLS == 0:
                print("Pausing to respect API call limits...")
                time.sleep(RATE_LIMIT_WINDOW)

    # Save player data locally
    output_file = f"{OUTPUT_PATH_ROOT}/players.json"
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(all_players_data, file, ensure_ascii=False, indent=4)

    print(f"Players data saved to {output_file}")

if __name__ == "__main__":
    print("Hello")
    collect_players_data()