from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from datetime import datetime
import sys
from dotenv import load_dotenv
import os 
from google.adk.models.lite_llm import LiteLlm
load_dotenv('/home/arvind/AI-agents-Dev/.env', override=False)
model = LiteLlm(
    model="openrouter/x-ai/grok-4-fast:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    """Get a nerdy joke about a specific topic."""
    print(f"--- Tool: get_nerd_joke called for topic: {topic} ---")

    # Example jokes - in a real implementation, you might want to use an API
    jokes = {
        "python": "Why don't Python programmers like to use inheritance? Because they don't like to inherit anything!",
        "javascript": "Why did the JavaScript developer go broke? Because he used up all his cache!",
        "java": "Why do Java developers wear glasses? Because they can't C#!",
        "programming": "Why do programmers prefer dark mode? Because light attracts bugs!",
        "math": "Why was the equal sign so humble? Because he knew he wasn't less than or greater than anyone else!",
        "physics": "Why did the photon check a hotel? Because it was travelling light!",
        "chemistry": "Why did the acid go to the gym? To become a buffer solution!",
        "biology": "Why did the cell go to therapy? Because it had too many issues!",
        "default": "Why did the computer go to the doctor? Because it had a virus!",
    }

    joke = jokes.get(topic.lower(), jokes["default"])

    # Update state with the last joke topic and persist conversation
    state = tool_context.state
    state["last_joke_topic"] = topic
    # Track delegation implicitly (manager delegated to funny_nerd)
    delegations = state.get("agent_delegations", [])
    delegations.append({
        "timestamp": datetime.now().isoformat(),
        "agent_name": "funny_nerd",
        "task": f"nerd_joke:{topic}",
        "status": "delegated"
    })
    state["agent_delegations"] = delegations
    history = state.get("conversation_history", [])
    history.append({
        "timestamp": datetime.now().isoformat(),
        "agent_name": "funny_nerd",
        "topic": topic,
        "agent_response": joke
    })
    state["conversation_history"] = history
    metadata = state.get("session_metadata", {})
    metadata["last_activity"] = datetime.now().isoformat()
    metadata["total_interactions"] = metadata.get("total_interactions", 0) + 1
    state["session_metadata"] = metadata

    return {"status": "success", "joke": joke, "topic": topic}


# Bring in preference tool so this agent can store preferences when asked
sys.path.append('/home/arvind/AI-agents-Dev/7.Multi-agent')
from state_management_tools import add_joke_preference

# Create the funny nerd agent
funny_nerd = Agent(
    name="funny_nerd",
    model=model,
    description="An agent that tells nerdy jokes about various topics.",
    instruction="""
    You are a funny nerd agent that tells nerdy jokes about various topics.
    
    When asked to tell a joke:
    1. Use the get_nerd_joke tool to fetch a joke about the requested topic
    2. If no specific topic is mentioned, ask the user what kind of nerdy joke they'd like to hear
    3. Format the response to include both the joke and a brief explanation if needed
    
    Available topics include:
    - python
    - javascript
    - java
    - programming
    - math
    - physics
    - chemistry
    - biology
    
    Example response format:
    "Here's a nerdy joke about <TOPIC>:
    <JOKE>
    
    Explanation: {brief explanation if needed}"

    If the user asks about anything else, 
    you should delegate the task to the manager agent.
    """,
    tools=[get_nerd_joke, add_joke_preference],
)