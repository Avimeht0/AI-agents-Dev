from datetime import datetime
from google.adk.tools.tool_context import ToolContext
from typing import List, Dict, Any

def track_agent_delegation(agent_name: str, task: str, tool_context: ToolContext) -> dict:
    """Track when the manager agent delegates tasks to sub-agents.
    
    Args:
        agent_name: Name of the agent being delegated to
        task: Description of the task being delegated
        tool_context: Context for accessing and updating session state
    
    Returns:
        A confirmation message with delegation details
    """
    print(f"--- Tool: track_agent_delegation called for {agent_name} with task: {task} ---")
    
    # Get current delegations from state
    delegations = tool_context.state.get("agent_delegations", [])
    
    # Create new delegation record
    delegation_record = {
        "timestamp": datetime.now().isoformat(),
        "agent_name": agent_name,
        "task": task,
        "status": "delegated"
    }
    
    # Add the new delegation
    delegations.append(delegation_record)
    
    # Update state with the new list of delegations
    tool_context.state["agent_delegations"] = delegations
    
    return {
        "action": "track_delegation",
        "agent_name": agent_name,
        "task": task,
        "message": f"Tracked delegation to {agent_name} for task: {task}",
        "total_delegations": len(delegations)
    }

def update_user_preferences(preference_type: str, value: Any, tool_context: ToolContext) -> dict:
    """Update user preferences for personalized agent interactions.
    
    Args:
        preference_type: Type of preference (favorite_agent, joke_preferences, etc.)
        value: The preference value to set
        tool_context: Context for accessing and updating session state
    
    Returns:
        A confirmation message
    """
    print(f"--- Tool: update_user_preferences called for {preference_type} with value: {value} ---")
    
    # Get current preferences from state
    preferences = tool_context.state.get("user_preferences", {})
    
    # Update the specific preference
    preferences[preference_type] = value
    
    # Update state with the modified preferences
    tool_context.state["user_preferences"] = preferences
    
    return {
        "action": "update_preferences",
        "preference_type": preference_type,
        "value": value,
        "message": f"Updated {preference_type} to: {value}"
    }

def add_to_stock_watchlist(ticker: str, tool_context: ToolContext) -> dict:
    """Add a stock ticker to the user's watchlist.
    
    Args:
        ticker: Stock ticker symbol to add
        tool_context: Context for accessing and updating session state
    
    Returns:
        A confirmation message
    """
    print(f"--- Tool: add_to_stock_watchlist called for {ticker} ---")
    
    # Get current watchlist from preferences
    preferences = tool_context.state.get("user_preferences", {})
    watchlist = preferences.get("stock_watchlist", [])
    
    # Add ticker if not already present
    if ticker.upper() not in [t.upper() for t in watchlist]:
        watchlist.append(ticker.upper())
        preferences["stock_watchlist"] = watchlist
        tool_context.state["user_preferences"] = preferences
        
        return {
            "action": "add_to_watchlist",
            "ticker": ticker.upper(),
            "message": f"Added {ticker.upper()} to your stock watchlist",
            "watchlist": watchlist
        }
    else:
        return {
            "action": "add_to_watchlist",
            "ticker": ticker.upper(),
            "message": f"{ticker.upper()} is already in your watchlist",
            "watchlist": watchlist
        }

def add_joke_preference(topic: str, tool_context: ToolContext) -> dict:
    """Add a joke topic to user preferences.
    
    Args:
        topic: Joke topic to add to preferences
        tool_context: Context for accessing and updating session state
    
    Returns:
        A confirmation message
    """
    print(f"--- Tool: add_joke_preference called for topic: {topic} ---")
    
    # Get current joke preferences
    preferences = tool_context.state.get("user_preferences", {})
    joke_preferences = preferences.get("joke_preferences", [])
    
    # Add topic if not already present
    if topic.lower() not in [t.lower() for t in joke_preferences]:
        joke_preferences.append(topic)
        preferences["joke_preferences"] = joke_preferences
        tool_context.state["user_preferences"] = preferences
        
        return {
            "action": "add_joke_preference",
            "topic": topic,
            "message": f"Added '{topic}' to your joke preferences",
            "joke_preferences": joke_preferences
        }
    else:
        return {
            "action": "add_joke_preference",
            "topic": topic,
            "message": f"'{topic}' is already in your joke preferences",
            "joke_preferences": joke_preferences
        }

def get_conversation_summary(tool_context: ToolContext) -> dict:
    """Get a summary of the conversation history.
    
    Args:
        tool_context: Context for accessing session state
    
    Returns:
        A summary of conversation history
    """
    print("--- Tool: get_conversation_summary called ---")
    
    # Get conversation history from state
    conversation_history = tool_context.state.get("conversation_history", [])
    delegations = tool_context.state.get("agent_delegations", [])
    metadata = tool_context.state.get("session_metadata", {})
    
    return {
        "action": "conversation_summary",
        "total_conversations": len(conversation_history),
        "total_delegations": len(delegations),
        "total_interactions": metadata.get("total_interactions", 0),
        "session_created": metadata.get("created_at", "Unknown"),
        "last_activity": metadata.get("last_activity", "Unknown"),
        "recent_delegations": delegations[-5:] if delegations else [],
        "message": f"Session has {len(conversation_history)} conversations and {len(delegations)} agent delegations"
    }

def set_favorite_agent(agent_name: str, tool_context: ToolContext) -> dict:
    """Set the user's favorite agent for future interactions.
    
    Args:
        agent_name: Name of the agent to set as favorite
        tool_context: Context for accessing and updating session state
    
    Returns:
        A confirmation message
    """
    print(f"--- Tool: set_favorite_agent called for {agent_name} ---")
    
    # Get current preferences
    preferences = tool_context.state.get("user_preferences", {})
    
    # Set favorite agent
    preferences["favorite_agent"] = agent_name
    tool_context.state["user_preferences"] = preferences
    
    return {
        "action": "set_favorite_agent",
        "agent_name": agent_name,
        "message": f"Set {agent_name} as your favorite agent",
        "favorite_agent": agent_name
    }

def get_agent_performance_stats(tool_context: ToolContext) -> dict:
    """Get performance statistics for different agents.
    
    Args:
        tool_context: Context for accessing session state
    
    Returns:
        Performance statistics for agents
    """
    print("--- Tool: get_agent_performance_stats called ---")
    
    # Get delegations from state
    delegations = tool_context.state.get("agent_delegations", [])
    
    # Count delegations by agent
    agent_counts = {}
    for delegation in delegations:
        agent_name = delegation.get("agent_name", "unknown")
        agent_counts[agent_name] = agent_counts.get(agent_name, 0) + 1
    
    # Get most used agent
    most_used_agent = max(agent_counts.items(), key=lambda x: x[1]) if agent_counts else ("none", 0)
    
    return {
        "action": "agent_performance_stats",
        "total_delegations": len(delegations),
        "agent_usage": agent_counts,
        "most_used_agent": most_used_agent[0],
        "most_used_count": most_used_agent[1],
        "message": f"Agent performance: {agent_counts} (Most used: {most_used_agent[0]} with {most_used_agent[1]} delegations)"
    }
