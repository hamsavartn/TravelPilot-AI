import re
from playwright.sync_api import Page, expect

def test_travelpilot_ui(page: Page):
    # Navigate to the app
    page.goto("http://localhost:8501")
    
    # Wait for the chat input to be visible and type the prompt
    page.get_by_placeholder("E.g., Plan a 3-day trip").fill("Plan a 3-day trip to Paris for $1000")
    page.get_by_placeholder("E.g., Plan a 3-day trip").press("Enter")
    
    # Wait for the agent to finish generating the itinerary
    page.wait_for_selector("text=Planning your trip...", state="hidden", timeout=30000)
    
    # Click the Disruption button
    page.get_by_text("🚨 Simulate Severe Weather (Rain)").click()
    
    # Wait for the warning to appear
    expect(page.locator("text=Agent Paused: Disruption Detected")).to_be_visible(timeout=15000)
    
    # Approve changes
    page.get_by_role("button", name="✅ Approve Changes").click()
    
    # Wait for the updated plan to appear
    expect(page.locator("text=Plan updated:")).to_be_visible(timeout=15000)
    
    print("✅ TravelPilot UI successfully verified via Playwright!")
