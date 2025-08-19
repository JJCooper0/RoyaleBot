import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("clash_royale_api_key")

class CR_Api_Handler:
    def __init__(self):
        pass

    def get_clan_riverracelog(self, clan_tag:str, limit:int=3):
        encoded_tag = clan_tag.replace("#", "%23")
        url = f"https://api.clashroyale.com/v1/clans/{encoded_tag}/riverracelog"

        headers = {
            "Authorization": f"Bearer {API_TOKEN}",
            "Accept": "application/json"
        }

        response = requests.get(
            url, 
            headers=headers, 
            params={"limit": limit}
        )

        if response.status_code == 200:
            return response.json()
        else:
            print("⚠️ api request failed!")
            print(response.json())
