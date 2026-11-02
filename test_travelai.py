import os
import requests
from dotenv import load_dotenv

load_dotenv()
AI_URL = os.getenv("AI_URL").rstrip("?")
API_KEY = os.getenv("API_KEY")

RUNS = 5  # how many times to try each prompt

origin, destination, duration = "Columbus", "Chicago", 3

tests = {
    "current app prompt": {
        "prompt": (
            f"Generate a travel itinerary from {origin} to {destination} in {duration} days. "
            "This is a road trip, keep it short, less than 15 lines, add some emojis "
            "(not more than 5) to make readable. If this requires a flight, please give "
            "priority to traveling to the airport by the shortest route and with fewer "
            "stops and maximizing time at the destination location. Public transportation "
            "will be used if the destination is in Europe or the UK. Otherwise, a rental "
            "car will be needed at the destination. Don't include costs of flights or "
            "rental cars to the cost per day. Add an estimated price of each day in both "
            "dollars and the destination currency."
        ),
        "context": (
            "You are a travel specialist and know the best tourist attractions around the "
            "world.You prioritize spending as much time as possible at or near the destination"
        ),
    },
    "new simple prompt": {
        "prompt": (
            f"{duration}-day trip from {origin} to {destination}. "
            "Max 12 lines, a few emojis. "
            "Estimated daily cost in USD and local currency."
        ),
        "context": "You are a concise travel specialist.",
    },
}

for name, params in tests.items():
    successes = 0
    print(f"\n=== {name} ===")
    for run in range(1, RUNS + 1):
        try:
            r = requests.get(AI_URL, params={**params, "key": API_KEY}, timeout=60)
            if r.ok:
                answer = r.json().get("answer", "").strip()
                if answer:
                    successes += 1
                print(f"  run {run}: {r.status_code} -> {len(answer)} chars: {answer[:80]!r}")
            else:
                print(f"  run {run}: {r.status_code} -> {r.text[:150]}")
        except Exception as e:
            print(f"  run {run}: ERROR {e}")
    print(f"  SCORE: {successes}/{RUNS} returned an itinerary")
    