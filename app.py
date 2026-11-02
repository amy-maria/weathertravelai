import os
import streamlit as st
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY")
API_KEY = os.getenv("API_KEY") or st.secrets.get("API_KEY")
API_URL = os.getenv("API_URL") or st.secrets.get("API_URL")
GEMINI_MODEL="gemini-3.5-flash-lite"


gemini = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=20000,                                
        retry_options=types.HttpRetryOptions(attempts=2),    
    ),
)


def get_current_weather(location):
    """Fetch real-time temperature and condition for a location."""
    
    try:
        response = requests.get(
            API_URL.rstrip("?"),
            params={"query": location, "key": API_KEY, "units": "imperial"},
            timeout=15,
        )
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": round(data["temperature"]["current"]),
                "condition": data["condition"]["description"]
            }
    except Exception:
        return None

def stream_itinerary(prompt, context):
    """Yield the itinerary text piece by piece as Gemini writes it."""
    stream = gemini.interactions.create(
        model=GEMINI_MODEL,
        system_instruction=context,
        input=prompt,
        generation_config={"thinking_level": "low"},
        stream=True,
    )
    for event in stream:
        if event.event_type == "step.delta" and event.delta.type == "text":
            yield event.delta.text.replace("$", r"\$")
            
# --- Streamlit UI Configurations ---
st.set_page_config(page_title="AI Road Trip Planner",
                   page_icon="🗺️", layout="centered")
st.title("🗺️ AI Road Trip Itinerary Planner")
st.write("Enter your route details below to dynamically generate metrics and custom AI summaries.")

# --- Interactive User Inputs (Pure Python!) ---
col1, col2 = st.columns(2)
with col1:
    origin = st.text_input("Starting City", placeholder="e.g., Paris")
with col2:
    destination = st.text_input("Destination City", placeholder="e.g., Rome")

duration = st.number_input("Trip Duration (Days)",
                           min_value=1, max_value=30, value=5)

# --- Action Button ---
if st.button("Generate Smart Itinerary", type="primary"):
    if not origin or not destination:
        st.error("Please enter both a starting city and a destination.")
    else:
        # Streamlit provides a native loading spinner wrapper
        with st.spinner("Compiling routing data and prompting AI Specialist..."):
            # --- NEW LOGIC: Clean up the destination for the Weather API ---
            # If the user types "Somerset, UK", this splits it at the comma
            # and takes just the first part ("Somerset"), stripping any extra spaces.
            weather_destination = destination.split(",")[0].strip()
            weather_origin = origin.split(",")[0].strip()
            # 1. Fetch Weather Data
            origin_weather = get_current_weather(weather_origin)
            dest_weather = get_current_weather(weather_destination)

            # Display Weather Side-by-Side
            w_col1, w_col2 = st.columns(2)
            with w_col1:
                st.subheader("Departure Weather")
                if origin_weather:
                    st.info(
                        f"**{origin.title()}:** {origin_weather['temp']} °F,  {origin_weather['condition']}")
                else:
                    st.write("Weather metrics unavailable.")
            with w_col2:
                st.subheader("Destination Weather")
                if dest_weather:
                    st.info(
                        f"**{destination.title()}:** {dest_weather['temp']} °F,  {dest_weather['condition']}")
                else:
                    st.write("Weather metrics unavailable.")

            # 2. Compile AI Prompt and fetch Itinerary
            prompt = f"Generate a travel itinerary from {origin} to {destination} in {duration} days. This is a road trip, keep it short, less than 15 lines, add some emojis (not more than 5) to make readable. If this requires a flight, please give priority to traveling to the airport by the shortest route and with fewer stops and maximizing time at the destination location. Public transportation will be used if the destination is in Europe or the UK. Otherwise, a rental car will be needed at the destination. Don't include costs of flights or rental cars to the cost per day. Add an estimated price of each day in both dollars and the destination currency.Format the answer as a Markdown bulleted list with one bullet per day, starting each bullet with the day in bold, like: - **Day 1:** ..."
            context = "You are a travel specialist and know the best tourist attractions around the world. You prioritize spending as much time as possible at or near the destination"
            
            try:
                st.subheader("Your Tailored Itinerary")
                itinerary_markdown = st.write_stream(stream_itinerary(prompt, context))
                
                if not itinerary_markdown:
                    st.warning("The AI didn't return an itinerary. Please try again.")

            except Exception as e:
                print(f"Gemini error: {e}")
                st.error("Sorry, the itinerary service is unavailable right now. Please try again shortly.")

st.divider()
st.caption(
    "The AI Travel Itinerary Planner was built by Amy Rowell and uses SheCodes Weather API and Gemini API for itinerary")
