# Multi-Agent Persistent Storage Implementation

## 🎯 Overview

This implementation demonstrates how to add persistent storage to a multi-agent system, showing the complete flow of sessions, state, events, and runners working together.

## 📁 Files Created

### Core Implementation
- **`persistent_multi_agent.py`** - Main persistent storage implementation
- **`state_management_tools.py`** - State management tools for multi-agent coordination
- **`demo_flow.py`** - Step-by-step demonstration script
- **`PERSISTENT_STORAGE_FLOW.md`** - Detailed flow explanation

### Updated Files
- **`manager/agent.py`** - Enhanced with state management tools

## 🏗️ Architecture Flow

```
Database (SQLite) ←→ Session Service ←→ Runner ←→ Multi-Agent System
     ↓                    ↓              ↓              ↓
State Storage ←→ Event Tracking ←→ Agent Delegation ←→ User Interaction
```

## 🔄 Complete Flow Explanation

### 1. **Database Storage**
- **SQLite Database**: `./multi_agent_data.db`
- **Purpose**: Persistent storage for all session data
- **Contains**: Sessions, states, events, conversation history

### 2. **Session Management**
- **Session Service**: `DatabaseSessionService`
- **Functions**:
  - `create_session()`: Creates new sessions with initial state
  - `get_session()`: Retrieves existing session data
  - `update_session()`: Updates session state
  - `list_sessions()`: Lists all sessions for a user

### 3. **Initial State**
```python
initial_state = {
    "user_name": "Arvind Mehta",
    "conversation_history": [],
    "agent_delegations": [],
    "user_preferences": {
        "favorite_agent": None,
        "joke_preferences": [],
        "stock_watchlist": [],
        "nerd_topics": []
    },
    "session_metadata": {
        "created_at": datetime.now().isoformat(),
        "last_activity": datetime.now().isoformat(),
        "total_interactions": 0
    }
}
```

### 4. **Runner Setup**
- **Purpose**: Orchestrates agent execution with session service
- **Key Functions**:
  - `run_async()`: Executes agents with session context
  - Manages event flow
  - Handles state updates

### 5. **Event Processing**
- **Tool Responses**: Track agent tool usage
- **Agent Delegations**: Record when manager delegates to sub-agents
- **State Updates**: Automatically update session state
- **Conversation History**: Maintain chat history

## 🚀 How to Run

### Option 1: Interactive Multi-Agent System
```bash
cd 7.Multi-agent
python persistent_multi_agent.py
```

### Option 2: Step-by-Step Demonstration
```bash
cd 7.Multi-agent
python demo_flow.py
```

## 🎭 Example Interaction Flow

```
User: "Tell me a joke about Python"
↓
Manager Agent: Delegates to funny_nerd
↓
State Update: track_agent_delegation("funny_nerd", "Python joke", context)
↓
Funny Nerd: Returns Python joke
↓
State Update: add_joke_preference("python", context)
↓
Database: All interactions saved to SQLite
↓
Next Session: User preferences and history are restored
```

## 🔧 State Management Tools

### Available Tools
1. **`track_agent_delegation`** - Track when manager delegates to sub-agents
2. **`update_user_preferences`** - Update user preferences for personalization
3. **`add_to_stock_watchlist`** - Add stocks to user's watchlist
4. **`add_joke_preference`** - Track user's joke topic preferences
5. **`get_conversation_summary`** - Get summary of conversation history
6. **`set_favorite_agent`** - Set user's preferred agent
7. **`get_agent_performance_stats`** - Get statistics about agent usage

### Usage in Manager Agent
```python
# When delegating to a sub-agent
track_agent_delegation("stock_analyst", "Get AAPL price", tool_context)

# When user shows preferences
add_joke_preference("python", tool_context)
add_to_stock_watchlist("AAPL", tool_context)
```

## 📊 State Structure

The persistent state includes:

```json
{
  "user_name": "Arvind Mehta",
  "conversation_history": [
    {
      "timestamp": "2024-01-15T10:30:00",
      "user_input": "Tell me a joke",
      "agent_response": "Why don't Python programmers...",
      "event_id": "event_123"
    }
  ],
  "agent_delegations": [
    {
      "timestamp": "2024-01-15T10:30:00",
      "agent_name": "funny_nerd",
      "task": "Tell Python joke",
      "status": "delegated"
    }
  ],
  "user_preferences": {
    "favorite_agent": "funny_nerd",
    "joke_preferences": ["python", "programming"],
    "stock_watchlist": ["AAPL", "GOOGL"],
    "nerd_topics": ["programming", "math"]
  },
  "session_metadata": {
    "created_at": "2024-01-15T10:00:00",
    "last_activity": "2024-01-15T10:30:00",
    "total_interactions": 5
  }
}
```

## 🎓 Key Learning Points

### 1. **Database Integration**
- How SQLite stores persistent data
- Session service manages database operations
- Data survives application restarts

### 2. **Session Management**
- Sessions are created, retrieved, and updated
- State is automatically persisted
- User data is maintained across conversations

### 3. **Event Flow**
- Events track agent interactions
- Tool responses are logged
- State updates are automatic

### 4. **Multi-Agent Coordination**
- Manager agent delegates to appropriate sub-agents
- State is shared across all agents
- Delegation history is maintained

### 5. **User Personalization**
- Preferences improve user experience
- Conversation history provides context
- Agent performance is tracked

## 🔍 What You'll See

### Before Running
- No database file exists
- No session data
- Fresh start

### After First Run
- Database file created: `./multi_agent_data.db`
- Session created with initial state
- User interactions logged
- Agent delegations tracked

### After Subsequent Runs
- Existing session restored
- Previous conversation history available
- User preferences maintained
- Agent performance statistics preserved

## 🚀 Next Steps

You can extend this system by:
- Adding new state management tools
- Creating additional agent types
- Implementing custom event handlers
- Adding more sophisticated user preference tracking
- Integrating with external databases (PostgreSQL, MongoDB, etc.)

## 📝 Summary

This implementation demonstrates the complete flow from database storage through session management to multi-agent coordination with persistent state. You now understand how:

1. **Sessions** manage user interactions across time
2. **State** persists user data and preferences
3. **Events** track agent responses and delegations
4. **Runners** orchestrate the entire system
5. **Database** provides persistent storage

The multi-agent system now has memory and can provide personalized experiences based on user history and preferences!
