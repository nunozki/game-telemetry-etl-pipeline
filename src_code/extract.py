import requests
from typing import Dict, Any, Optional, List
from datetime import datetime

class SteamDataExtractor:
    """
    Class responsible for extracting telemetry data from the public Steam API.
    """
    
    def __init__(self, timeout: int = 10):
        # The base_url is stored in the class state
        self.base_url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
        self.timeout = timeout
        
        # PRO TIP: Using a Session improves performance by reusing TCP connections (Connection Pooling)
        self.session = requests.Session()
        print("🔌 SteamDataExtractor successfully initialized.")

    def fetch_player_count(self, app_id: int) -> Optional[Dict[str, Any]]:
        """
        Extracts the number of active players for a single App ID.
        """
        params = {"appid": app_id}
        
        try:
            # We use the session instead of a standalone requests.get()
            response = self.session.get(self.base_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            
            # Validate if the expected payload structure exists
            if "response" in data and "player_count" in data["response"]:
                return {
                    "app_id": app_id,
                    "player_count": data["response"]["player_count"],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                print(f"⚠️ Warning: The API did not return 'player_count' for App ID {app_id}.")
                return None
                
        except requests.exceptions.RequestException as e:
            # RequestException catches all HTTP, Connection, and Timeout errors at once
            print(f"❌ Error accessing App ID {app_id}: {e}")
            return None

    def extract_multiple_games(self, games_dict: Dict[int, str]) -> List[Dict[str, Any]]:
        """
        Utility method to extract data from a list of games and return it as a structured list.
        """
        extracted_records = []
        
        for app_id, game_name in games_dict.items():
            print(f"Extracting data for: {game_name} (ID: {app_id})...")
            result = self.fetch_player_count(app_id)
            
            if result:
                print(f"  -> Success! {result['player_count']} players online.")
                extracted_records.append(result)
            else:
                print(f"  -> Failed to extract data for {game_name}.")
                
        return extracted_records