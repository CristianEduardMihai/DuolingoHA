import requests
import json
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Constants from .env
DUOLINGO_USER = os.getenv("DUOLINGO_USER")
HA_URL = os.getenv("HA_URL")
HA_TOKEN = os.getenv("HA_TOKEN")

# API Endpoints
HA_URL_NUMBER = f"{HA_URL}/api/services/input_number/set_value"
HA_URL_BINARY_ON = f"{HA_URL}/api/services/input_boolean/turn_on"
HA_URL_BINARY_OFF = f"{HA_URL}/api/services/input_boolean/turn_off"
DUOLINGO_URL = f"https://www.duolingo.com/2017-06-30/users?username={DUOLINGO_USER}"

# Headers for the Home Assistant REST API
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_user_data():
    try:
        # Specify additional headers to avoid 406 error
        request_headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        response = requests.get(DUOLINGO_URL, headers=request_headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None

def update_ha_input_number(streak_length):
    try:
        data = {
            "entity_id": "input_number.duolingo_streak",
            "value": streak_length
        }
        response = requests.post(HA_URL_NUMBER, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"Successfully updated the input number: {streak_length} days")
        else:
            print(f"Failed to update the input number. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error updating input number: {e}")

def update_ha_binary_sensor(practiced_today):
    try:
        url = HA_URL_BINARY_ON if practiced_today else HA_URL_BINARY_OFF
        data = {
            "entity_id": "input_boolean.duolingo_practiced_today"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            print(f"Successfully updated the binary sensor: {'on' if practiced_today else 'off'}")
        else:
            print(f"Failed to update the binary sensor. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error updating binary sensor: {e}")

def main():
    user_data = fetch_user_data()
    if user_data and "users" in user_data:
        user = user_data["users"][0]
        streak_length = user["streakData"]["currentStreak"]["length"]
        streak_end_date = user["streakData"]["currentStreak"]["endDate"]
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        practiced_today = (streak_end_date == current_date)
        
        update_ha_input_number(streak_length)
        update_ha_binary_sensor(practiced_today)

if __name__ == "__main__":
    main()
