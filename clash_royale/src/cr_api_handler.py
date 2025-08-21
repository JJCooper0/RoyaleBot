import os
import requests
import json
from dotenv import load_dotenv

name_buffer = {} # player_tag -> player_name

class CR_Api_Handler:
    def __init__(self):
        load_dotenv()
        self.API_TOKEN = os.getenv("clash_royale_api_key")

    def _api_get_request(self, request: str, params: dict | None = None):
        url = f"https://api.clashroyale.com/v1/{request}"
        headers = {
            "Authorization": f"Bearer {self.API_TOKEN}",
            "Accept": "application/json"
        }
        if params:
            response = requests.get(url, headers=headers, params=params)
        else:
            response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            response_json = ""
            try:
                response_json = response.json()
            except:
                response_json = f"❌ Couldn't read response JSON. Status code: {response.status_code}"
            raise Exception(f"⚠️ API Request failed!\n{response_json}")
        
    def buffer_name(self, player_tag, player_name):
        """
        This function maps the player names to their tags to avoid multiple API requests. 
        To be called whenever the information is accessible anyway.
        """
        if player_tag in name_buffer and player_name != name_buffer[player_tag]:
            raise Exception(f"⚠️ Player name doesn't match with the previous entry for this tag!\n For tag {player_tag}: previous: {name_buffer[player_tag]}, new: {player_name}")
        name_buffer[player_tag] = player_name
    
    def get_clan_riverracelog(self, clan_tag: str, number_of_weeks: int = 3):
        encoded_tag = str(clan_tag).replace("#", "%23")
        params = {"limit": number_of_weeks}
        return self._api_get_request(request=f"clans/{encoded_tag}/riverracelog", params=params)

    def get_player_name(self, player_tag: str):
        if player_tag in name_buffer:
            return name_buffer[player_tag]
        else:
            print(f"⚠️ Player tag {player_tag} was not buffered! Avoid unnecessary API requests!")
            encoded_tag = str(player_tag).replace("#", "%23")
            return self._api_get_request(request=f"players/{encoded_tag}")["name"]