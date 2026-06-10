# 🗺️ AI Weather and Travel Itinerary Planner

A dynamic, intelligent Single Page Application (SPA) built entirely in Python using Streamlit. This application uses multiple third-party API handshakes to deliver unified travel itineraries synced alongside real-time departure and arrival weather metrics.

## 🚀 Live Demo
Experience the live dashboard deployed on my Portfolio: 
amyrowell.dev

---

## 💡 Technical Competencies Demonstrated

* **Data Engineering & Input Cleansing:** Implemented Python string parsing (`.split().strip()`) to decouple conversational user entry from external API syntax constraints. The application gracefully accepts regional qualifiers (e.g., `Somerset, UK`) to preserve geographical intent for the AI Agent, while programmatically filtering the location down to clean string formats for the Weather API engine to eliminate runtime faults.
* **Rapid Prototype Micro-Frontend Architecture:** Leveraged Streamlit's structural execution tree to design a fully interactive, reactive user experience directly in Python, bypassing HTML/CSS/JS frameworks while preserving premium responsive design paradigms.
* **Multi-API Orchestration:** Coordinated concurrent RESTful JSON data handshakes across multiple endpoints (SheCodes WeatherAPI & Generative AI Models), gracefully handling independent error margins and fallbacks for each.
* **Environment Configuration & Token Isolation:** Maintained strict security isolation by concealing platform API keys locally inside standard `.env` blocks and deploying natively across cloud server environment contexts.


## 🛠️ Tech Stack & Dependencies

* **Core Framework:** Streamlit
* **Data Retrieval:** Requests (RESTful API Handshake Management)
* **API Providers:** SheCodes Weather API, SheCodes AI Service

