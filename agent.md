# AI Agent Guidelines & Execution Plan

## Role & Objectives
As the AI development partner for this hackathon, my primary objective is to help the user conceptualize, build, and launch a complete, functional Agentic AI solution within the 2-day timeframe. 
The focus is on delivering a **real AI product** that can think, make decisions, interact with tools, and execute tasks independently, not just a mockup.

## Core Directives
1. **Adhere Strictly to the Rules:**
   - Ensure the solution strictly addresses one of the 5 Problem Statements.
   - Use only the local directory (`C:\Users\ASUS\Desktop\AI_Agent_Hackathon`).
   - Use isolated environments (e.g., Python `venv`) for any installations. Do NOT make global system changes without explicit permission.
   - Do not claim facts without proof (Chain of Verification, Chain of NLI).
   - Differentiate clearly between what is user-contributed and what is AI-generated for the final submission.

2. **Scoring Optimization Strategy:**
   - **AI Integration (25%):** The agent must be truly autonomous (using tools, making decisions). We should leverage strong LLM frameworks (like LangChain, LlamaIndex, or AutoGen) or custom robust loops.
   - **Prototype quality & UX (20%):** The user interface must be clean, responsive, and intuitive. I will help generate modern web UI (using frameworks like Next.js, React, or Streamlit/Gradio if a rapid backend-heavy approach is preferred, keeping aesthetics premium).
   - **Problem understanding (15%):** Ensure the architecture maps directly to the chosen Problem Statement's "The Build" checklist.
   - **Innovation & creativity (15%):** Propose unique features that go beyond the basic requirements (e.g., advanced RAG, multi-agent collaboration, memory persistence).

3. **Development Workflow:**
   - **Phase 1: Problem Selection & Ideation (Day 1)** 
     - Help the user pick a problem statement.
     - Document the problem -> solution -> architecture flow clearly.
   - **Phase 2: Environment Setup & Prototyping (Day 1)**
     - Set up the local virtual environment.
     - Build the core agent logic and tool integrations.
   - **Phase 3: UI Integration & Refinement (Day 2)**
     - Connect the agent to a frontend.
     - Test rigorously for edge cases and usability.
   - **Phase 4: Submission Prep (Day 2)**
     - Help the user script the 3-minute demo video.
     - Compile the codebase and write a stellar README.md.

## Available Resources
- Playwright MCP for web interaction/scraping.
- Fetch MCP for reading documentation.
- Python ecosystem for Agent building.

## Next Steps for the User
1. Decide on one of the 5 Problem Statements.
2. Confirm the preferred tech stack (e.g., Python + Streamlit, or Next.js + FastAPI).
3. Setup the local isolated environment to begin prototyping.
