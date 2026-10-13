# TravelPilot ✈️

TravelPilot is an autonomous multi-agent travel planner built with LangGraph and Streamlit. It solves complex constraints and handles real-time disruptions (e.g., severe weather) using Human-in-the-Loop (HITL) architecture.

## Features
- **Multi-Agent Orchestration:** Specialized agents for Planning, Searching, Constraint Management, and Budget Checking.
- **Human-In-The-Loop (HITL):** When disruptions occur, the graph pauses, alerts the user, and waits for approval before replanning.
- **Interactive UI:** Built with Streamlit and PyDeck (Mapbox) for beautiful geospatial rendering.

## Setup Instructions

1. **Install Dependencies:**
   Make sure you have Python 3.12 installed, then run:
   ```bash
   py -3.12 -m venv venv_stable
   # On Windows:
   venv_stable\Scripts\activate
   # On Mac/Linux:
   source venv_stable/bin/activate
   
   pip install -r requirements.txt
   ```

2. **Configure API Keys:**
   Your `.env` file is already populated with the necessary keys (Gemini, OpenWeatherMap, Mapbox, SerpApi).

3. **Run the App:**
   ```bash
   streamlit run app.py
   ```
