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

## Demo Script (3-Minute Video)
1. **0:00 - 0:30:** Open the app. Show the UI and explain the architecture (LangGraph handling state and specialized agents).
2. **0:30 - 1:30:** Type a query: "Plan a 3-day trip to Paris for $1000". Wait for the LLM to generate the itinerary and map waypoints.
3. **1:30 - 2:30:** Click the **"🚨 Simulate Severe Weather"** button. Explain how this injects state into the LangGraph and triggers the `budget_checker` node to interrupt execution.
4. **2:30 - 3:00:** Show the HITL buttons appearing. Click **Approve** and watch the agent dynamically replan the trip. End recording.
