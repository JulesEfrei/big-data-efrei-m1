import requests
import json
import os
from main import OUTPUT_PATH_ROOT

def fetch_champions(version='latest', language='en_US'):
    if version == "latest":
        res = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        versions = res.json()
        version = versions[0]

    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{language}/champion.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        champions_data = response.json()["data"]

        champions_list = []
        for champion_name, data in champions_data.items():
            champions_list.append({
                "champion_name": champion_name,
                "data": data
            })

        file_path = os.path.join(OUTPUT_PATH_ROOT, 'champions.json')
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(champions_list, file, ensure_ascii=False, indent=4)
        
        print(f"Champions data fetched and saved to {file_path}.")
    else:
        print(f"Failed to fetch champions data. Status code: {response.status_code}")

if __name__ == "__main__":
    fetch_champions()