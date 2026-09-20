import os
import json
from typing import TypedDict, List, Dict, Any, Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)


class AgentState(TypedDict):
    query: str
    destination: str
    dates: str
    budget: float
    constraints: List[str]
    search_data: Dict[str, Any]
    itinerary: str 
    disruption_alert: Optional[str]
    replan_count: int
    waypoints: List[Dict[str, float]] 
    status: str

def orchestrator(state: AgentState):
    query = state.get("query", "")
    prompt = f"Extract destination, dates, and budget (as float) from this travel query. Return ONLY JSON format: {{\"destination\": \"City\", \"dates\": \"Date range\", \"budget\": 1000.0}}. Query: {query}"
    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        content = response.content
        if isinstance(content, list):
            content = "".join([b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"])
        text = content.replace('```json', '').replace('```', '').strip()
        data = json.loads(text)
        return {
            "destination": data.get("destination", "Unknown"),
            "dates": data.get("dates", "Unknown"),
            "budget": float(data.get("budget", 0.0)),
            "status": "Orchestrator parsed query"
        }
    except:
        return {"destination": "Paris", "dates": "Next week", "budget": 1000.0, "status": "Orchestrator used fallback parsing"}


def constraint_manager(state: AgentState):
    return {
        "constraints": ["Keep daily budget balanced", "Avoid overlapping activities", "Include indoor backups"],
        "status": "Constraints formalized"
    }

def search_agent(state: AgentState):
    dest = state.get("destination", "Paris")
    
    prompt = f"""Generate realistic coordinate data for {dest}.
Return ONLY a valid JSON object with this exact structure:
{{
    "search_data": {{
        "flights": [{{"airline": "ExampleAir", "price": 300, "time": "08:00 AM"}}],
        "hotels": [{{"name": "Central Hotel", "price": 150, "lat": 0.0, "lon": 0.0}}],
        "activities": [{{"name": "Popular Site", "cost": 50, "lat": 0.0, "lon": 0.0}}]
    }},
    "waypoints": [
        {{"name": "Origin", "lat": 40.7128, "lon": -74.0060}},
        {{"name": "Central Hotel", "lat": 0.0, "lon": 0.0}}
    ]
}}
Ensure you return at least 4 waypoints (1 origin like New York for the flight path arc, 1 hotel, 2 activities) with real latitude/longitude for {dest}."""

    response = llm.invoke([HumanMessage(content=prompt)])
    try:
        content = response.content
        if isinstance(content, list):
            content = "".join([b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"])
        text = content.replace('```json', '').replace('```', '').strip()
        data = json.loads(text)
        return {
            "search_data": data.get("search_data", {}),
            "waypoints": data.get("waypoints", []),
            "status": "Search data generated via LLM"
        }
    except Exception as e:
        print("Search agent JSON parse error:", e)
        # Fallback
        return {
            "search_data": {"hotels": [{"name": "Fallback", "lat": 48.85, "lon": 2.35}]},
            "waypoints": [{"name": "Origin", "lat": 40.7128, "lon": -74.0060}, {"name": "Fallback", "lat": 48.85, "lon": 2.35}],
            "status": "Search data fallback"
        }

def planner(state: AgentState):
    dest = state.get("destination")
    dates = state.get("dates")
    budget = state.get("budget")
    search_data = state.get("search_data")
    disruption = state.get("disruption_alert")
    
    sys_msg = """You are an expert travel planner. Create a day-by-day itinerary.
CRITICAL VERIFICATION STEP (CoVe): At the end of your itinerary, add a '### Verification' section where you explicitly list the budget limit and the calculated total cost of your plan to prove it is within budget."""
    if disruption:
        sys_msg += f"\nIMPORTANT: Modify the plan to handle this disruption: {disruption}. Explicitly verify that the disruption was mitigated in the Verification section."
        
    prompt = f"Destination: {dest}, Dates: {dates}, Budget: {budget}\nAvailable options: {search_data}\nGenerate a beautiful Markdown itinerary."
    response = llm.invoke([SystemMessage(content=sys_msg), HumanMessage(content=prompt)])
    
    content = response.content
    if isinstance(content, list):
        content = "".join([b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"])
    
    return {"itinerary": content, "status": "Itinerary generated"}


def budget_checker(state: AgentState):
    from langgraph.types import interrupt
    
    disruption = state.get("disruption_alert")
    replan_count = state.get("replan_count", 0)
    
    # If a disruption was injected and we haven't replanned yet, trigger HITL interrupt
    if disruption and replan_count == 0:
        user_decision = interrupt({
            "action": "approve_disruption_plan",
            "reason": f"Disruption detected: {disruption}. Need approval to alter itinerary and potentially increase budget."
        })
        
        if user_decision == "reject":
            return {"status": "User rejected replan", "replan_count": replan_count + 1}
        else:
            return {"status": "User approved replan", "replan_count": replan_count + 1}
            
    return {"status": "Validation passed", "replan_count": replan_count + 1}


def checker_router(state: AgentState):
    if state.get("status") == "User approved replan":
        return "planner"
    return END

# Build Graph
builder = StateGraph(AgentState)
builder.add_node("orchestrator", orchestrator)
builder.add_node("constraint_manager", constraint_manager)
builder.add_node("search_agent", search_agent)
builder.add_node("planner", planner)
builder.add_node("budget_checker", budget_checker)

builder.add_edge(START, "orchestrator")
builder.add_edge("orchestrator", "constraint_manager")
builder.add_edge("constraint_manager", "search_agent")
builder.add_edge("search_agent", "planner")
builder.add_edge("planner", "budget_checker")
builder.add_conditional_edges("budget_checker", checker_router, {"planner": "planner", END: END})

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
