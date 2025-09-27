import os
import requests
from dotenv import load_dotenv
from datetime import datetime, date
from zoneinfo import ZoneInfo

load_dotenv()
api_key = os.getenv("API_KEY")

def get_classement():
    uri_classement = 'https://api.football-data.org/v4/competitions/PL/standings'
    headers = {'X-Auth-Token': api_key}

    try:
        response = requests.get(uri_classement, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Erreur API classement:", e)
        return None
    
    data = response.json()
    classement = data['standings'][0]['table']
    result = []
    
    for team in classement:
        position = team['position']
        name = team['team']['name']
        points = team['points']
        result.append((position, name, points))
        
    return result
    
        
def get_match_today():
    uri_matches = 'https://api.football-data.org/v4/teams/57/matches'
    headers = {'X-Auth-Token': api_key}
    response = requests.get(uri_matches, headers=headers)
    data = response.json()
    matches = data['matches']

    # today = datetime.now(ZoneInfo("Europe/London")).date()
    today = date(2025, 9, 28) # test
    
    for match in matches:
        match_date = datetime.fromisoformat(match['utcDate'].replace('Z', '+00:00')).date()
        if match_date == today:
            return match
    return None