from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.joke_agent.agent import joke_agent
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time

# Import state management tools
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from state_management_tools import (
    track_agent_delegation,
    update_user_preferences,
    add_to_stock_watchlist,
    add_joke_preference,
    get_conversation_summary,
    set_favorite_agent,
    get_agent_performance_stats,
    log_user_input,
)

from dotenv import load_dotenv
import os 
from google.adk.models.lite_llm import LiteLlm
load_dotenv('/home/arvind/AI-agents-Dev/.env', override=False)
model = LiteLlm(
    model="openrouter/x-ai/grok-4-fast:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

root_agent = Agent(
    name="manager",
    model=model,
    description="Manager agent with persistent state management",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents.
    You have access to persistent state management tools that help track user interactions,
    preferences, and agent delegations across conversations.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agents:
    - stock_analyst: For stock price queries and financial information
    - funny_nerd: For nerdy jokes about programming, science, and technology
    - joke_agent: For general jokes and humor

    **STATE MANAGEMENT CAPABILITIES:**
    You have access to tools that help maintain persistent state:
    - track_agent_delegation: Track when you delegate tasks to sub-agents
    - update_user_preferences: Update user preferences for personalized interactions
    - add_to_stock_watchlist: Add stocks to user's watchlist
    - add_joke_preference: Track user's joke topic preferences
    - get_conversation_summary: Get summary of conversation history
    - set_favorite_agent: Set user's preferred agent
    - get_agent_performance_stats: Get statistics about agent usage

    **DELEGATION WORKFLOW:**
    1. ALWAYS call log_user_input with the user's exact message BEFORE doing anything else
    2. When delegating to a sub-agent, use track_agent_delegation first
    3. Use appropriate tools to update user preferences based on their requests
    4. Provide personalized responses based on stored preferences
    5. Track user interactions to improve future responses

    **PERSONALIZATION:**
    - Remember user preferences across conversations
    - Use stored preferences to provide better recommendations
    - Track which agents the user prefers for different tasks
    - Maintain conversation history for context

    You also have access to the following basic tools:
    - get_current_time: Get current timestamp
    """,
    sub_agents=[stock_analyst, funny_nerd, joke_agent],
    tools=[
        get_current_time,
        log_user_input,
        track_agent_delegation,
        update_user_preferences,
        add_to_stock_watchlist,
        add_joke_preference,
        get_conversation_summary,
        set_favorite_agent,
        get_agent_performance_stats,
    ],
)