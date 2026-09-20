import streamlit as st
import pydeck as pdk
import os
from langchain_core.messages import HumanMessage
from langgraph.types import Command
import uuid

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import the LangGraph agent
from agent import graph

st.set_page_config(page_title="TravelPilot ✈️", layout="wide", initial_sidebar_state="expanded")

# Glassmorphism CSS injection
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #151520 100%);
        color: #ffffff;
        font-family: 'Inter', sans-serif;
    }
    
    /* Glassmorphism containers */
    .stChatFloatingInputContainer {
        background: rgba(30, 30, 45, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stChatMessage {
        background: rgba(45, 45, 65, 0.6) !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Disruption button glow */
    .stButton>button {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(255, 65, 108, 0.4) !important;
        transition: all 0.3s ease !important;
        border-radius: 8px !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 65, 108, 0.6) !important;
    }
</style>
""", unsafe_allow_html=True)

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! I'm TravelPilot. Where would you like to go?"}]
if "waypoints" not in st.session_state:
    st.session_state.waypoints = []

config = {"configurable": {"thread_id": st.session_state.thread_id}}

def render_map(waypoints):
    if not waypoints:
        st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(latitude=48.8566, longitude=2.3522, zoom=2, pitch=45)))
        return
    
    arcs = []
    if len(waypoints) > 1:
        origin = waypoints[0]
        for wp in waypoints[1:]:
            arcs.append({
                "source": [origin["lon"], origin["lat"]],
                "target": [wp["lon"], wp["lat"]],
                "name": f"From {origin.get('name', 'Origin')} to {wp.get('name', 'Destination')}"
            })
            
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=waypoints,
        get_position="[lon, lat]",
        get_color="[0, 200, 255, 200]",
        get_radius=15000,
        pickable=True,
    )
    
    arc_layer = pdk.Layer(
        "ArcLayer",
        data=arcs,
        get_source_position="source",
        get_target_position="target",
        get_source_color="[255, 65, 108, 200]",
        get_target_color="[0, 200, 255, 200]",
        get_width=5,
        pickable=True
    )
    
    view_state = pdk.ViewState(latitude=waypoints[0]["lat"], longitude=waypoints[0]["lon"], zoom=3, pitch=45, bearing=15)
    st.pydeck_chart(pdk.Deck(layers=[scatter_layer, arc_layer], initial_view_state=view_state, map_provider="mapbox", api_keys={"mapbox": os.getenv("MAPBOX_API_KEY")}))

col1, col2 = st.columns([1, 2])

with col1:
    st.header("🌍 Itinerary Map")
    render_map(st.session_state.waypoints)
    
    st.markdown("---")
    st.subheader("Disruption Simulation")
    st.write("Click below to simulate a severe weather event and trigger the agent's Human-In-The-Loop (HITL) replanning.")
    if st.button("🚨 Simulate Severe Weather (Rain)"):
        # Invoke the graph again with the disruption alert and reset replan_count
        query = st.session_state.messages[-1]["content"] if st.session_state.messages else "Plan a trip"
        graph.invoke({"query": query, "disruption_alert": "Severe Rainstorm tomorrow afternoon. Avoid outdoor activities.", "replan_count": 0}, config)
        st.rerun()

with col2:
    st.header("TravelPilot Chat")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            content = msg["content"]
            if isinstance(content, list):
                content = "".join([b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"])
            st.markdown(content)
            
    # Check if we are currently interrupted by LangGraph
    state_snapshot = graph.get_state(config)
    
    if state_snapshot.next:
        # Agent is paused waiting for user input
        st.warning("🚨 **Agent Paused: Disruption Detected**")
        st.write("The agent has detected a weather disruption and generated a contingency plan. Do you approve the changes?")
        c1, c2 = st.columns(2)
        if c1.button("✅ Approve Changes"):
            # Resume execution with the command
            result = graph.invoke(Command(resume="approve"), config)
            # The agent will have replanned and updated the itinerary
            if "itinerary" in result:
                st.session_state.messages.append({"role": "assistant", "content": "Plan updated:\n" + result["itinerary"]})
            st.rerun()
        if c2.button("❌ Reject"):
            result = graph.invoke(Command(resume="reject"), config)
            if "itinerary" in result:
                st.session_state.messages.append({"role": "assistant", "content": "Disruption ignored. Keeping original plan."})
            st.rerun()
    else:
        # Normal chat input
        if prompt := st.chat_input("E.g., Plan a 3-day trip to Paris for $1000"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            with st.chat_message("assistant"):
                with st.spinner("Planning your trip..."):
                    # Initial state for the graph
                    result = graph.invoke({"query": prompt}, config)
                    itinerary = result.get("itinerary", "Sorry, I encountered an issue.")
                    if isinstance(itinerary, list):
                        itinerary = "".join([b.get("text", "") for b in itinerary if isinstance(b, dict) and b.get("type") == "text"])
                    st.markdown(itinerary)
                    st.session_state.messages.append({"role": "assistant", "content": itinerary})
                    if "waypoints" in result:
                        st.session_state.waypoints = result["waypoints"]
                    st.rerun()
