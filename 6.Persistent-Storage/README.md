# Persistent Storage Agent - Complete Guide

This directory demonstrates a sophisticated AI agent system with persistent storage, session management, state handling, and event-driven architecture. The agent can remember conversations across multiple sessions and maintain user data persistently.

## 📁 Directory Structure

```
6.Persistent-Storage/
├── main.py                    # Main application entry point
├── utils.py                   # Utility functions for state display and event processing
├── memory_agent/             # Agent module
│   ├── __init__.py           # Package initialization
│   └── agent.py              # Agent implementation with tools
├── my_agent_data.db          # SQLite database for persistent storage
└── README.md                  # This comprehensive guide
```

## 🏗️ Architecture Overview

### Core Components

1. **Session Service** - Manages persistent sessions across conversations
2. **State Management** - Maintains user data and conversation context
3. **Agent Runner** - Orchestrates agent execution and event handling
4. **Event System** - Processes real-time events during agent interactions
5. **Tool System** - Provides agent capabilities for state manipulation

## 🔧 Detailed Component Explanations

### 1. Session Management

**What is a Session?**
A session represents a continuous conversation between a user and the agent. Sessions persist across application restarts and maintain conversation history.

**Session Lifecycle:**
```python
# Session Creation Process
1. Check for existing sessions for the user
2. If found: Continue with existing session
3. If not found: Create new session with initial state
4. Session persists in SQLite database
```

**Key Features:**
- **Persistent Storage**: Sessions survive application restarts
- **User Isolation**: Each user has separate sessions
- **State Continuity**: Conversation context is maintained
- **Session Recovery**: Can resume previous conversations

### 2. State Management

**What is State?**
State represents the current data and context that the agent maintains for each user. It includes user information, conversation history, and any persistent data.

**State Structure:**
```python
initial_state = {
    "user_name": "Arvind Mehta",    # User's name
    "reminders": [],                # List of user reminders
    # Additional state can be added here
}
```

**State Operations:**
- **Read State**: Access current user data
- **Update State**: Modify user information
- **Persist State**: Save changes to database
- **State Recovery**: Load previous state on session resume

### 3. Event System

**What are Events?**
Events are real-time notifications that occur during agent execution. They provide insight into what the agent is doing and allow for real-time monitoring.

**Event Types:**
- **Tool Events**: When agent calls tools
- **Response Events**: When agent generates responses
- **State Events**: When state is modified
- **Error Events**: When errors occur

**Event Processing:**
```python
async for event in runner.run_async(user_id, session_id, message):
    # Process each event in real-time
    response = await process_agent_response(event)
```

### 4. Agent Runner

**What is a Runner?**
A runner is the orchestration layer that manages agent execution, session handling, and event processing. It connects the agent to the session service and manages the execution flow.

**Runner Responsibilities:**
- **Agent Execution**: Runs the agent with proper context
- **Session Management**: Handles session creation and retrieval
- **Event Streaming**: Processes events in real-time
- **State Synchronization**: Ensures state consistency

## 🛠️ Available Tools

The agent has access to several tools for managing user data:

### 1. `add_reminder(reminder: str)`
- **Purpose**: Adds a new reminder to the user's list
- **Parameters**: `reminder` - The reminder text
- **State Impact**: Adds to `reminders` list in state
- **Example**: `add_reminder("Buy groceries")`

### 2. `view_reminders()`
- **Purpose**: Displays all current reminders
- **Parameters**: None
- **State Impact**: Read-only operation
- **Example**: Shows numbered list of reminders

### 3. `update_reminder(index: int, updated_text: str)`
- **Purpose**: Modifies an existing reminder
- **Parameters**: 
  - `index` - 1-based index of reminder to update
  - `updated_text` - New reminder text
- **State Impact**: Modifies specific reminder in list
- **Example**: `update_reminder(1, "Buy organic groceries")`

### 4. `delete_reminder(index: int)`
- **Purpose**: Removes a reminder from the list
- **Parameters**: `index` - 1-based index of reminder to delete
- **State Impact**: Removes reminder from list
- **Example**: `delete_reminder(2)`

### 5. `update_user_name(name: str)`
- **Purpose**: Updates the user's name in state
- **Parameters**: `name` - New user name
- **State Impact**: Updates `user_name` in state
- **Example**: `update_user_name("John Doe")`

## 🚀 Complete Real-World Example: "Remind me to buy milk"

Let's trace through a complete, real example showing exactly what happens when a user says "Remind me to buy milk". This will show you the actual data structures, events, and state changes.

### 📊 Initial Session State (Before Request)

```json
{
  "session_id": "sess_abc123",
  "app_name": "Memory Agent", 
  "user_id": "arvind_rajesh_mehta",
  "state": {
    "user_name": "Arvind Mehta",
    "reminders": []
  }
}
```

### 🔄 Complete Event Flow: "Remind me to buy milk"

#### **Event 1: Agent Acknowledgment**
```json
{
  "id": "evt_001",
  "author": "agent",
  "content": {
    "parts": [
      {
        "text": "Sure! I'll add that reminder for you."
      }
    ]
  },
  "is_final_response": false
}
```

#### **Event 2: Tool Request**
```json
{
  "id": "evt_002", 
  "author": "agent",
  "content": {
    "parts": [
      {
        "tool_request": {
          "name": "add_reminder",
          "arguments": {
            "reminder": "buy milk"
          }
        }
      }
    ]
  },
  "is_final_response": false
}
```

#### **Tool Execution (Internal)**
```python
# Runner executes the tool internally
tool_context = ToolContext(session=session, state=state)
result = add_reminder("buy milk", tool_context)

# Inside add_reminder function:
def add_reminder(reminder: str, tool_context: ToolContext):
    reminders = tool_context.state.get("reminders", [])
    reminders.append(reminder)  # ["buy milk"]
    tool_context.state["reminders"] = reminders
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": "Added reminder: buy milk"
    }
```

#### **Event 3: Tool Response**
```json
{
  "id": "evt_003",
  "author": "tool", 
  "content": {
    "parts": [
      {
        "tool_response": {
          "action": "add_reminder",
          "reminder": "buy milk",
          "message": "Added reminder: buy milk"
        }
      }
    ]
  },
  "is_final_response": false
}
```

#### **State Persistence (Internal)**
```python
# Runner persists the updated state to database
session_service.update_session(
    app_name="Memory Agent",
    user_id="arvind_rajesh_mehta", 
    session_id="sess_abc123",
    state={
        "user_name": "Arvind Mehta",
        "reminders": ["buy milk"]  # Updated!
    }
)
```

#### **Event 4: Final Agent Response**
```json
{
  "id": "evt_004",
  "author": "agent",
  "content": {
    "parts": [
      {
        "text": "Perfect! I've added 'buy milk' to your reminders. You now have 1 reminder."
      }
    ]
  },
  "is_final_response": true
}
```

### 📊 Final Session State (After Request)

```json
{
  "session_id": "sess_abc123",
  "app_name": "Memory Agent",
  "user_id": "arvind_rajesh_mehta", 
  "state": {
    "user_name": "Arvind Mehta",
    "reminders": ["buy milk"]
  }
}
```

### 🔍 Visual Event Timeline

```
User Input: "Remind me to buy milk"
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Event 1: Agent Text                                         │
│ "Sure! I'll add that reminder for you."                    │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Event 2: Tool Request                                      │
│ add_reminder(reminder="buy milk")                          │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Tool Execution (Internal)                                  │
│ • Get current reminders: []                               │
│ • Add "buy milk": ["buy milk"]                            │
│ • Update state: state["reminders"] = ["buy milk"]         │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Event 3: Tool Response                                     │
│ {"action": "add_reminder", "message": "Added reminder"}   │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ State Persistence (Internal)                              │
│ Database updated with new state                            │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ Event 4: Final Response                                   │
│ "Perfect! I've added 'buy milk' to your reminders."       │
└─────────────────────────────────────────────────────────────┘
```

### 🛠️ Code Implementation Flow

#### **Step 1: Session Creation**
```python
# Application startup
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# Check for existing session or create new one
existing_sessions = session_service.list_sessions(
    app_name="Memory Agent",
    user_id="arvind_rajesh_mehta"
)

if existing_sessions and len(existing_sessions.sessions) > 0:
    SESSION_ID = existing_sessions.sessions[0].id
    print(f"Continuing existing session: {SESSION_ID}")
else:
    initial_state = {"user_name": "Arvind Mehta", "reminders": []}
    new_session = session_service.create_session(
        app_name="Memory Agent",
        user_id="arvind_rajesh_mehta", 
        state=initial_state
    )
    SESSION_ID = new_session.id
    print(f"Created new session: {SESSION_ID}")
```

#### **Step 2: Runner Setup**
```python
# Create runner with agent and session service
runner = Runner(
    agent=memory_agent,
    app_name="Memory Agent",
    session_service=session_service
)
```

#### **Step 3: Event Processing**
```python
async def call_agent_async(runner, user_id, session_id, query):
    # Display state before processing
    display_state(runner.session_service, runner.app_name, user_id, session_id, "BEFORE")
    
    # Process agent with event streaming
    async for event in runner.run_async(
        user_id=user_id, 
        session_id=session_id, 
        new_message=Content(role="user", parts=[Part(text=query)])
    ):
        response = await process_agent_response(event)
        if response:
            final_response_text = response
    
    # Display state after processing  
    display_state(runner.session_service, runner.app_name, user_id, session_id, "AFTER")
```

#### **Step 4: Event Processing Function**
```python
async def process_agent_response(event):
    print(f"Event ID: {event.id}, Author: {event.author}")
    
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "text") and part.text:
                print(f"  Text: {part.text}")
            if hasattr(part, "tool_request") and part.tool_request:
                print(f"  Tool Request: {part.tool_request}")
            if hasattr(part, "tool_response") and part.tool_response:
                print(f"  Tool Response: {part.tool_response}")
    
    if event.is_final_response():
        print("  → This is the final response")
        return event.content.parts[0].text.strip()
    
    return None
```

## 📊 State Display Example

The system provides detailed state visualization:

```
---------- Current State ----------
👤 User: Arvind Mehta
📝 Reminders:
  1. Buy groceries
  2. Call mom
  3. Finish project report
------------------------------
```

## 🔄 Complete Workflow Example

### Scenario: User adds a reminder and views their list

1. **User Input**: "Add a reminder to buy milk"
2. **State Before**: `{"user_name": "Arvind", "reminders": ["Buy groceries"]}`
3. **Agent Processing**: 
   - Calls `add_reminder("buy milk")`
   - Updates state: `{"user_name": "Arvind", "reminders": ["Buy groceries", "buy milk"]}`
4. **State After**: `{"user_name": "Arvind", "reminders": ["Buy groceries", "buy milk"]}`
5. **Agent Response**: "I've added 'buy milk' to your reminders. You now have 2 reminders."

### Event Flow During Processing:
```
1. Tool Event: add_reminder called for 'buy milk'
2. State Update: reminders list updated
3. Tool Response: {"action": "add_reminder", "reminder": "buy milk", "message": "Added reminder: buy milk"}
4. Final Response: Agent generates user-friendly response
```

## 🗄️ Database Schema & Real Data Examples

### SQLite Database Structure

The `my_agent_data.db` file contains these tables:

#### **Sessions Table**
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    app_name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    state TEXT NOT NULL,  -- JSON serialized state
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### **Sample Session Data**
```sql
INSERT INTO sessions VALUES (
    'sess_abc123',
    'Memory Agent', 
    'arvind_rajesh_mehta',
    '{"user_name": "Arvind Mehta", "reminders": ["buy milk", "call mom"]}',
    '2024-01-15 10:30:00',
    '2024-01-15 10:35:00'
);
```

#### **Messages Table**
```sql
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'user', 'agent', 'tool'
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
```

#### **Sample Message Data**
```sql
-- User message
INSERT INTO messages VALUES (
    'msg_001',
    'sess_abc123',
    'user',
    'Remind me to buy milk',
    '2024-01-15 10:30:00'
);

-- Agent response
INSERT INTO messages VALUES (
    'msg_002', 
    'sess_abc123',
    'agent',
    'Perfect! I have added "buy milk" to your reminders.',
    '2024-01-15 10:30:05'
);
```

### 🔍 Complete Working Example with Real Output

Here's what you'll see when running the application:

#### **Terminal Output Example**
```bash
$ python main.py

Welcome to Memory Agent Chat!
Your reminders will be remembered across conversations.
Type 'exit' or 'quit' to end the conversation.

---------- State BEFORE processing ----------
👤 User: Arvind Mehta
📝 Reminders: None
----------------------------------------

--- Running Query: Remind me to buy milk ---
Event ID: evt_001, Author: agent
  Text: Sure! I'll add that reminder for you.

Event ID: evt_002, Author: agent  
  Tool Request: {'name': 'add_reminder', 'arguments': {'reminder': 'buy milk'}}
--- Tool: add_reminder called for 'buy milk' ---

Event ID: evt_003, Author: tool
  Tool Response: {'action': 'add_reminder', 'reminder': 'buy milk', 'message': 'Added reminder: buy milk'}

Event ID: evt_004, Author: agent
  Text: Perfect! I've added 'buy milk' to your reminders. You now have 1 reminder.
  → This is the final response

╔══ AGENT RESPONSE ═════════════════════════════════════════
Perfect! I've added 'buy milk' to your reminders. You now have 1 reminder.
╚═════════════════════════════════════════════════════════════

---------- State AFTER processing ----------
👤 User: Arvind Mehta  
📝 Reminders:
  1. buy milk
----------------------------------------

You: Show my reminders
---------- State BEFORE processing ----------
👤 User: Arvind Mehta
📝 Reminders:
  1. buy milk
----------------------------------------

--- Running Query: Show my reminders ---
Event ID: evt_005, Author: agent
  Tool Request: {'name': 'view_reminders', 'arguments': {}}
--- Tool: view_reminders called ---

Event ID: evt_006, Author: tool
  Tool Response: {'action': 'view_reminders', 'reminders': ['buy milk'], 'count': 1}

Event ID: evt_007, Author: agent
  Text: Here are your current reminders:
1. buy milk
  → This is the final response

╔══ AGENT RESPONSE ═════════════════════════════════════════
Here are your current reminders:
1. buy milk
╚═════════════════════════════════════════════════════════════

---------- State AFTER processing ----------
👤 User: Arvind Mehta
📝 Reminders:
  1. buy milk
----------------------------------------

You: exit
Ending conversation. Your data has been saved to the database.
```

#### **Database State After Session**
```sql
-- Sessions table
SELECT * FROM sessions;
```
```
id          | app_name     | user_id              | state                                    | created_at          | updated_at
sess_abc123 | Memory Agent | arvind_rajesh_mehta  | {"user_name": "Arvind Mehta", "reminders": ["buy milk"]} | 2024-01-15 10:30:00 | 2024-01-15 10:35:00
```

```sql
-- Messages table  
SELECT * FROM messages;
```
```
id      | session_id   | role  | content                                    | created_at
msg_001 | sess_abc123  | user  | Remind me to buy milk                     | 2024-01-15 10:30:00
msg_002 | sess_abc123  | agent | Perfect! I've added 'buy milk' to your... | 2024-01-15 10:30:05
msg_003 | sess_abc123  | user  | Show my reminders                          | 2024-01-15 10:35:00
msg_004 | sess_abc123  | agent | Here are your current reminders: 1. buy...| 2024-01-15 10:35:05
```

## 🚀 Running the Application

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   ```bash
   # Create .env file with your API keys
   OPENROUTER_API_KEY=your_api_key_here
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

4. **Interactive Usage**:
   ```
   Welcome to Memory Agent Chat!
   Your reminders will be remembered across conversations.
   Type 'exit' or 'quit' to end the conversation.

   You: Hello, I'm John
   Agent: Hello John! I've updated your name. How can I help you today?

   You: Add a reminder to buy groceries
   Agent: I've added 'buy groceries' to your reminders. You now have 1 reminder.

   You: Show my reminders
   Agent: Here are your current reminders:
   1. buy groceries

   You: exit
   Ending conversation. Your data has been saved to the database.
   ```

## 🔧 Advanced Features

### State Persistence
- Data survives application restarts
- Multiple users can have separate sessions
- State is automatically synchronized

### Event Monitoring
- Real-time event processing
- Tool execution tracking
- State change notifications
- Error handling and reporting

### Session Recovery
- Automatic session detection
- State restoration on restart
- Conversation continuity

## 🎯 Learning Objectives

This implementation teaches:
- **Session Management**: How to maintain persistent conversations
- **State Handling**: Managing user data across interactions
- **Event Processing**: Real-time monitoring of agent execution
- **Tool Integration**: Creating agent capabilities
- **Database Operations**: Persistent storage with SQLite
- **Async Programming**: Handling asynchronous operations
- **Agent Architecture**: Building sophisticated AI agents

## 🔍 Complete Traceable Example: Step-by-Step Debugging

### 🎯 Example Scenario: "Add reminder to call mom"

Let's trace through a complete example with all the internal details:

#### **Step 1: Session Loading**
```python
# Runner loads existing session
session = session_service.get_session(
    app_name="Memory Agent",
    user_id="arvind_rajesh_mehta", 
    session_id="sess_abc123"
)

# Current state loaded from database
current_state = {
    "user_name": "Arvind Mehta",
    "reminders": ["buy milk"]
}
```

#### **Step 2: User Input Processing**
```python
# User input wrapped into Content object
user_input = "Add a reminder to call mom"
content = Content(
    role="user",
    parts=[Part(text="Add a reminder to call mom")]
)
```

#### **Step 3: Agent Processing - Event Stream**

**Event 1: Agent Thinking**
```json
{
  "id": "evt_008",
  "author": "agent", 
  "content": {
    "parts": [{"text": "I'll add that reminder for you."}]
  },
  "is_final_response": false
}
```

**Event 2: Tool Request**
```json
{
  "id": "evt_009",
  "author": "agent",
  "content": {
    "parts": [{
      "tool_request": {
        "name": "add_reminder",
        "arguments": {"reminder": "call mom"}
      }
    }]
  },
  "is_final_response": false
}
```

**Event 3: Tool Execution (Internal)**
```python
# Runner creates tool context
tool_context = ToolContext(session=session, state=current_state)

# Tool function executes
def add_reminder(reminder: str, tool_context: ToolContext):
    # Get current reminders: ["buy milk"]
    reminders = tool_context.state.get("reminders", [])
    
    # Add new reminder: ["buy milk", "call mom"]
    reminders.append(reminder)
    
    # Update state
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": "Added reminder: call mom"
    }
```

**Event 4: Tool Response**
```json
{
  "id": "evt_010",
  "author": "tool",
  "content": {
    "parts": [{
      "tool_response": {
        "action": "add_reminder",
        "reminder": "call mom", 
        "message": "Added reminder: call mom"
      }
    }]
  },
  "is_final_response": false
}
```

**Event 5: State Persistence (Internal)**
```python
# Runner persists updated state to database
updated_state = {
    "user_name": "Arvind Mehta",
    "reminders": ["buy milk", "call mom"]
}

session_service.update_session(
    app_name="Memory Agent",
    user_id="arvind_rajesh_mehta",
    session_id="sess_abc123", 
    state=updated_state
)
```

**Event 6: Final Response**
```json
{
  "id": "evt_011",
  "author": "agent",
  "content": {
    "parts": [{
      "text": "Great! I've added 'call mom' to your reminders. You now have 2 reminders."
    }]
  },
  "is_final_response": true
}
```

#### **Step 4: Final State**
```json
{
  "session_id": "sess_abc123",
  "state": {
    "user_name": "Arvind Mehta", 
    "reminders": ["buy milk", "call mom"]
  }
}
```

### 🐛 Debugging & Troubleshooting

#### **Common Issues & Solutions:**

1. **Database Connection Issues**
   ```bash
   # Check if database file exists
   ls -la my_agent_data.db
   
   # Test database connection
   sqlite3 my_agent_data.db "SELECT COUNT(*) FROM sessions;"
   ```

2. **Session Not Found**
   ```python
   # Debug session lookup
   sessions = session_service.list_sessions(app_name="Memory Agent", user_id="user123")
   print(f"Found {len(sessions.sessions)} sessions")
   for session in sessions.sessions:
       print(f"Session: {session.id}, State: {session.state}")
   ```

3. **State Not Persisting**
   ```python
   # Check if state is being updated
   print("State before tool:", tool_context.state)
   # ... tool execution ...
   print("State after tool:", tool_context.state)
   ```

4. **Event Processing Issues**
   ```python
   # Debug event processing
   async def debug_process_agent_response(event):
       print(f"Event ID: {event.id}")
       print(f"Author: {event.author}")
       print(f"Is Final: {event.is_final_response()}")
       
       if event.content and event.content.parts:
           for i, part in enumerate(event.content.parts):
               print(f"Part {i}: {part}")
   ```

#### **Debug Features Available:**

1. **State Display**
   ```python
   # Shows current state before/after processing
   display_state(session_service, app_name, user_id, session_id, "DEBUG")
   ```

2. **Event Logging**
   ```python
   # Log all events with details
   async for event in runner.run_async(...):
       print(f"Event: {event.id} | Author: {event.author} | Final: {event.is_final_response()}")
   ```

3. **Tool Execution Tracking**
   ```python
   # Each tool call is logged
   print(f"--- Tool: {tool_name} called for '{args}' ---")
   ```

4. **Database Inspection**
   ```sql
   -- Check session state
   SELECT id, state FROM sessions WHERE user_id = 'arvind_rajesh_mehta';
   
   -- Check message history
   SELECT role, content, created_at FROM messages 
   WHERE session_id = 'sess_abc123' 
   ORDER BY created_at;
   ```

### 🎯 Key Learning Points

1. **Session = Persistent Container**: Sessions survive application restarts
2. **State = Agent Memory**: State contains all user data and preferences  
3. **Events = Real-time Stream**: Events show what's happening as it happens
4. **Runner = Orchestrator**: Runner manages everything and creates events
5. **Tools = Agent Capabilities**: Tools modify state and return results

### 🔧 Production Considerations

1. **Concurrent Access**: Multiple users can have separate sessions
2. **State Size**: Large state objects may impact performance
3. **Error Handling**: Tools should handle errors gracefully
4. **Persistence**: State changes are automatically persisted
5. **Memory Management**: Old sessions can be archived or deleted

This comprehensive system demonstrates how to build production-ready AI agents with persistent memory, session management, and sophisticated state handling capabilities.