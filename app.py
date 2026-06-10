import os
import streamlit as st
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
AI_URL = os.getenv("AI_URL")


def get_current_weather(location):
    """Fetch real-time temperature and condition for a location."""
    api_url = f"{API_URL}query={location}&key={API_KEY}&units=imperial"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return {
                "temp": round(data["temperature"]["current"]),
                "condition": data["condition"]["description"]
            }
    except Exception:
        return None


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
            prompt = f"Generate a travel itinerary from {origin} to {destination} in {duration} days. This is a road trip, keep it short, less than 15 lines, add some emojis (not more than 5) to make readable. If this requires a flight, please give priority to traveling to the airport by the shortest route and with fewer stops and maximizing time at the destination location. Public transportation will be used if the destination is in Europe or the UK. Otherwise, a rental car will be needed at the destination. Don't include costs of flights or rental cars to the cost per day. Add an estimated price of each day in both dollars and the destination currency."
            context = "You are a travel specialist and know the best tourist attractions around the world.You prioritize spending as much time as possible at or near the destination"
            ai_url = f"{AI_URL}prompt={prompt}&context={context}&key={API_KEY}"

            try:
                ai_response = requests.get(ai_url)
                ai_data = ai_response.json()
                itinerary_markdown = ai_data.get(
                    "answer", "Failed to generate itinerary text.")

                # 3. Render Output (Streamlit reads Markdown formatting natively!)
                st.success("📋 Your Tailored Itinerary")
                st.markdown(itinerary_markdown)

            except Exception as e:
                st.error(f"Error communicating with AI Agent: {str(e)}")

st.divider()
st.caption(
    "The AI Travel Itinerary Planner was built by Matt Delac & adapted by Amy Rowell 💖")
