import os
import requests
from dotenv import load_dotenv

load_dotenv()
AI_URL = os.getenv("AI_URL").rstrip("?")
API_KEY = os.getenv("API_KEY")

tests = {
    "1 tiny":   {"prompt": "Say hello in five words.", "context": "Be brief."},
    "2 medium": {"prompt": "Plan a 3 day road trip from Columbus to Chicago.",
                 "context": "You are a travel specialist."},
    "3 no context": {"prompt": "Say hello in five words."},
        "4 app prompt": {
        "prompt": "Generate a travel itinerary from Columbus to Chicago in 3 days. This is a road trip, keep it short, less than 15 lines, add some emojis (not more than 5) to make readable. If this requires a flight, please give priority to traveling to the airport by the shortest route and with fewer stops and maximizing time at the destination location. Public transportation will be used if the destination is in Europe or the UK. Otherwise, a rental car will be needed at the destination. Don't include costs of flights or rental cars to the cost per day. Add an estimated price of each day in both dollars and the destination currency.",
        "context": "You are a travel specialist and know the best tourist attractions around the world.You prioritize spending as much time as possible at or near the destination",
    },
    "5 short travel": {
        "prompt": "3-day road trip Columbus to Chicago. Max 10 lines. Daily cost in USD.",
        "context": "You are a concise travel specialist.",
    },
}

for name, params in tests.items():
    try:
        r = requests.get(AI_URL, params={**params, "key": API_KEY}, timeout=60)
        answer = r.json().get("answer", "") if r.ok else r.text[:200]
        print(f"{name}: {r.status_code} -> {len(answer)} chars: {answer[:150]}")
    except Exception as e:
        print(f"{name}: ERROR {e}")
