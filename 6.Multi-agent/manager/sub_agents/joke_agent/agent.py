import os
import random
from dotenv import load_dotenv

from google.adk.models.lite_llm import LiteLlm
from google.adk import Agent
from google.adk.tools.tool_context import ToolContext
from datetime import datetime
import sys


# Load environment variables from root .env
load_dotenv('/home/arvind/AI-agents-Dev/.env', override=False)

# Define the tool function
def bad_jokes(tool_context: ToolContext) -> str:
    jokes_list = [
        "Why don't skeletons fight each other? - They don't have the guts.",
        "I'm reading a book about anti-gravity. It's impossible to put down.",
        "Why did the scarecrow win an award? - Because he was outstanding in his field!",
        "What's orange and sounds like a parrot? - A carrot.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don't programmers like nature? - It has too many bugs.",
        "I told my computer I needed a break. - Now it won't stop sending me Kit-Kats.",
        "Why was the math book sad? - Because it had too many problems.",
        "What do you call fake spaghetti? - An impasta."
    ]
    joke = random.choice(jokes_list)

    # Persist minimal conversation info
    state = tool_context.state
    # Track delegation implicitly (manager delegated to joke_agent)
    delegations = state.get("agent_delegations", [])
    delegations.append({
        "timestamp": datetime.now().isoformat(),
        "agent_name": "joke_agent",
        "task": "tell_joke",
        "status": "delegated"
    })
    state["agent_delegations"] = delegations

    history = state.get("conversation_history", [])
    history.append({
        "timestamp": datetime.now().isoformat(),
        "agent_name": "joke_agent",
        "agent_response": joke
    })
    state["conversation_history"] = history

    metadata = state.get("session_metadata", {})
    metadata["last_activity"] = datetime.now().isoformat()
    metadata["total_interactions"] = metadata.get("total_interactions", 0) + 1
    state["session_metadata"] = metadata

    # Also store last joke for convenience
    state["last_joke"] = joke

    return joke

# Model setup (OpenRouter)
model = LiteLlm(
    model="openrouter/x-ai/grok-4-fast:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Bring in preference tool so this agent can store preferences when asked
sys.path.append('/home/arvind/AI-agents-Dev/7.Multi-agent')
from state_management_tools import add_joke_preference

# Agent definition (just pass the function directly)
joke_agent = Agent(
    name="joke_agent",
    model=model,
    description="Tool agent that tells jokes",
    instruction="""
    You are a helpful assistant that can use the following tool:
    - bad_jokes: returns a random joke.
    When someone asks for a joke, always call the tool and print the result directly.

    If the user asks to save or add this joke or a topic to preferences,
    call add_joke_preference(topic) with the most relevant topic word(s) from the request.
    """,
    tools=[bad_jokes, add_joke_preference],  # ✅ Pass the functions directly
)
root_agent = joke_agent