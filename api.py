import requests
import re
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Constants from .env
DUOLINGO_USER = os.getenv("DUOLINGO_USER")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

HA_URL = HA_URL + "/api/services/input_number/set_value"
DUOLINGO_URL = F"https://duolingo-stats-card.vercel.app/api?username={DUOLINGO_USER}"
# Headers for the Home Assistant REST API
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_streak():
    try:
        response = requests.get(DUOLINGO_URL)
        html_content = response.text
        streak_pattern = re.compile(r'(\d+)\s+Day streak')
        match = streak_pattern.search(html_content)
        if match:
            return match.group(1)
        else:
            print("Streak days not found in the HTML content.")
            return None
    except Exception as e:
        print(f"Error fetching streak days: {e}")
        return None

def update_ha_input_number(streak_days):
    try:
        data = {
            "entity_id": "input_number.duolingo_streak",
            "value": int(streak_days)
        }
        response = requests.post(HA_URL, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"Successfully updated the input number: {streak_days} days")
        else:
            print(f"Failed to update the input number. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error updating input number: {e}")

streak_days = fetch_streak()
if streak_days is not None:
  update_ha_input_number(streak_days)