from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

from dotenv import load_dotenv
import os 
from google.adk.models.lite_llm import LiteLlm
load_dotenv('/home/arvind/AI-agents-Dev/.env', override=False)
model = LiteLlm(
    model="openrouter/x-ai/grok-4-fast:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def get_stock_price(ticker: str, tool_context: ToolContext) -> dict:
    """Retrieves current stock price and saves to session state."""
    print(f"--- Tool: get_stock_price called for {ticker} ---")

    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")

        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch price for {ticker}",
            }

        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        result = {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": current_time,
        }

        # Persist to state: watchlist and history + delegation log
        state = tool_context.state
        delegations = state.get("agent_delegations", [])
        delegations.append({
            "timestamp": datetime.now().isoformat(),
            "agent_name": "stock_analyst",
            "task": f"get_stock_price:{ticker}",
            "status": "delegated"
        })
        state["agent_delegations"] = delegations
        preferences = state.get("user_preferences", {})
        watchlist = preferences.get("stock_watchlist", [])
        if ticker.upper() not in [t.upper() for t in watchlist]:
            watchlist.append(ticker.upper())
            preferences["stock_watchlist"] = watchlist
            state["user_preferences"] = preferences

        price_history = state.get("price_history", [])
        price_history.append(result)
        state["price_history"] = price_history

        metadata = state.get("session_metadata", {})
        metadata["last_activity"] = datetime.now().isoformat()
        metadata["total_interactions"] = metadata.get("total_interactions", 0) + 1
        state["session_metadata"] = metadata

        return result

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching stock data: {str(e)}",
        }


# Create the root agent
stock_analyst = Agent(
    name="stock_analyst",
    model=model,
    description="An agent that can look up stock prices and track them over time.",
    instruction="""
    You are a helpful stock market assistant that helps users track their stocks of interest.
    
    When asked about stock prices:
    1. Use the get_stock_price tool to fetch the latest price for the requested stock(s)
    2. Format the response to show each stock's current price and the time it was fetched
    3. If a stock price couldn't be fetched, mention this in your response
    
    Example response format:
    "Here are the current prices for your stocks:
    - GOOG: $175.34 (updated at 2024-04-21 16:30:00)
    - TSLA: $156.78 (updated at 2024-04-21 16:30:00)
    - META: $123.45 (updated at 2024-04-21 16:30:00)"
    """,
    tools=[get_stock_price],
)