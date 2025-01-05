import os
import json
import time
import requests
import signal
import sys
from main import API_KEY, OUTPUT_PATH_ROOT, RATE_LIMIT_CALLS, RATE_LIMIT_WINDOW

# Global variables
PROCESSED_FILE = './data/bronze/processed_puuids.json'
PLAYERS_FILE = './data/bronze/players.json'  # Path to players.json

# Function to load processed PUUIDs from the file
def load_processed_puuids():
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

# Function to save processed PUUIDs to the file
def save_processed_puuids(processed_puuids):
    with open(PROCESSED_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(processed_puuids), f, ensure_ascii=False, indent=4)

# Function to read player data from players.json
def load_players():
    if os.path.exists(PLAYERS_FILE):
        with open(PLAYERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []  # Return an empty list if the file doesn't exist

# Fetch recent matches for a player
def fetch_recent_matches(puuid, region):

    if region == "euw1":
        region = "europe"
    else:
        region = "asia"

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=50&api_key={API_KEY}"
    
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))
            print(f"Rate limit reached. Sleeping for {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"Error {response.status_code} for puuid {puuid}")
            return []

# Fetch match details for a match ID
def fetch_match_details(match_id, region):

    if region == "euw1":
        region = "europe"
    else:
        region = "asia"

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"
    
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 10))
            print(f"Rate limit reached. Sleeping for {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            print(f"Error {response.status_code} for match ID {match_id}")
            return None

# Function to process players and fetch matches
def process_matches(players):
    processed_puuids = load_processed_puuids()

    for player in players:
        puuid = player['puuid']
        player_match_data = []
        
        # Skip if player has already been processed
        if puuid in processed_puuids:
            print(f"Skipping {puuid}, already processed.")
            continue
        
        print(f"Fetching matches for player {puuid} (Region: {player['region']})")
        
        # Fetch match IDs
        match_ids = fetch_recent_matches(puuid, player['region'])
        
        for match_id in match_ids:
            match_data = fetch_match_details(match_id, player['region'])
            
            if match_data:
                match_data['player_puuid'] = puuid
                player_match_data.append(match_data)
            
            # Sleep to respect rate limits
            time.sleep(0.2)

        # After fetching all matches for the player, mark them as processed
        processed_puuids.add(puuid)

        # Save processed PUUIDs to file after each player
        save_processed_puuids(processed_puuids)

        # Rate limit handling
        if len(player_match_data) % RATE_LIMIT_CALLS == 0:
            print("Pausing to respect rate limits...")
            time.sleep(RATE_LIMIT_WINDOW)

    # Save match data to file (or database)
    matches_file = OUTPUT_PATH_ROOT + 'matches.json'
    with open(matches_file, 'a', encoding='utf-8') as f:
        json.dump(player_match_data, f, ensure_ascii=False, indent=4)

    print(f"Match data saved to {matches_file}")

# Main execution
if __name__ == "__main__":
    # Load players from players.json
    players = load_players()

    if players:
        process_matches(players)
    else:
        print("No players found. Make sure players.json is present and contains valid data.")