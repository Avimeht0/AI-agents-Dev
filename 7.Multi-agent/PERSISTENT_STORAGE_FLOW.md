# Multi-Agent Persistent Storage Flow Explanation

This document explains how sessions, state, events, and runners work together in the multi-agent system with persistent storage.

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    PERSISTENT STORAGE FLOW                   │
├─────────────────────────────────────────────────────────────┤
│  1. Database (SQLite) ←→ 2. Session Service ←→ 3. Runner   │
│     ↓                    ↓                    ↓            │
│  4. State Storage ←→ 5. Event Tracking ←→ 6. Agent Exec  │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Components Breakdown

### 1. **Database Storage (SQLite)**
- **Purpose**: Persistent storage for all session data
- **Location**: `./multi_agent_data.db`
- **Contains**: Sessions, states, events, conversation history

### 2. **Session Service**
- **Purpose**: Manages session lifecycle and state persistence
- **Key Functions**:
  - `create_session()`: Creates new sessions with initial state
  - `get_session()`: Retrieves existing session data
  - `update_session()`: Updates session state
  - `list_sessions()`: Lists all sessions for a user

### 3. **Initial State**
- **Purpose**: Defines the starting state for new sessions
- **Contains**:
  - User information
  - Conversation history
  - Agent delegation tracking
  - User preferences
  - Session metadata

### 4. **Runner**
- **Purpose**: Orchestrates agent execution with session service
- **Key Functions**:
  - `run_async()`: Executes agents with session context
  - Manages event flow
  - Handles state updates

### 5. **Events**
- **Purpose**: Track agent responses and state changes
- **Types**:
  - Tool responses
  - Agent delegations
  - State updates
  - Final responses

## 🔄 Complete Flow Example

### Step 1: Database Initialization
```python
# Create SQLite database connection
db_url = "sqlite:///./multi_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)
```

### Step 2: Session Management
```python
# Check for existing sessions
existing_sessions = session_service.list_sessions(
    app_name="Multi-Agent System",
    user_id="arvind_rajesh_mehta"
)

# Create new session if none exists
if not existing_sessions:
    new_session = session_service.create_session(
        app_name="Multi-Agent System",
        user_id="arvind_rajesh_mehta",
        state=initial_state
    )
```

### Step 3: Runner Setup
```python
# Create runner with session service
runner = Runner(
    agent=root_agent,
    app_name="Multi-Agent System",
    session_service=session_service
)
```

### Step 4: Event Processing
```python
# Process user input through multi-agent system
async for event in runner.run_async(
    user_id=user_id, 
    session_id=session_id, 
    new_message=content
):
    # Track agent delegations
    if event.author == "manager":
        track_agent_delegation("stock_analyst", "Get stock price", tool_context)
    
    # Update conversation history
    conversation_history.append({
        "timestamp": datetime.now().isoformat(),
        "user_input": user_input,
        "agent_response": event.content.parts[0].text,
        "event_id": event.id
    })
```

### Step 5: State Persistence
```python
# Update session state
session_service.update_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id,
    state=updated_state
)
```

## 🎯 Key Features Demonstrated

### 1. **Session Persistence**
- Sessions survive across application restarts
- User data is maintained between conversations
- Agent delegation history is preserved

### 2. **State Management**
- User preferences are stored and retrieved
- Conversation history is maintained
- Agent performance is tracked

### 3. **Event Tracking**
- All agent interactions are logged
- Delegation patterns are recorded
- User preferences are updated automatically

### 4. **Multi-Agent Coordination**
- Manager agent delegates to appropriate sub-agents
- State is shared across all agents
- Delegation history is maintained

## 🚀 How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   # Create .env file with your API keys
   OPENROUTER_API_KEY=your_api_key_here
   ```

3. **Run the Persistent Multi-Agent System**:
   ```bash
   cd 7.Multi-agent
   python persistent_multi_agent.py
   ```

## 📝 Example Interaction Flow

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

## 🔍 State Structure

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

## 🎓 Learning Points

1. **Database Integration**: How SQLite stores persistent data
2. **Session Management**: How sessions are created, retrieved, and updated
3. **State Persistence**: How application state survives restarts
4. **Event Flow**: How events track agent interactions
5. **Multi-Agent Coordination**: How agents work together with shared state
6. **User Personalization**: How preferences improve user experience

## 🔧 Customization

You can extend this system by:
- Adding new state management tools
- Creating additional agent types
- Implementing custom event handlers
- Adding more sophisticated user preference tracking
- Integrating with external databases (PostgreSQL, MongoDB, etc.)

This implementation demonstrates the complete flow from database storage through session management to multi-agent coordination with persistent state!
