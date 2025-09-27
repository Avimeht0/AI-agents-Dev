# 4. Sessions and State

This directory demonstrates how to create AI agents with memory and state management capabilities, enabling persistent conversations and context awareness.

## 📁 Contents

### Agent Module
- `question_answering_agent/` - Agent with session and state management
  - `__init__.py` - Package initialization file
  - `agent.py` - Main agent class with stateful capabilities

### Additional Files
- `basic_stateful_session.py` - Basic implementation of stateful sessions

## ✨ Features

- **Session Management**: Maintains conversation context across interactions
- **State Persistence**: Remembers user preferences and conversation history
- **Context Awareness**: Uses previous conversation context for better responses
- **Memory Management**: Efficiently stores and retrieves conversation data
- **Session Recovery**: Can resume conversations after interruptions
- **Multi-user Support**: Handles multiple concurrent user sessions

## 🚀 Usage

### Quick Start

1. **Import the question answering agent:**
   ```python
   from question_answering_agent import agent
   ```

2. **Create and use the agent:**
   ```python
   # Initialize the agent
   agent = agent.QuestionAnsweringAgent()
   
   # Start a session
   session_id = agent.create_session("user123")
   
   # Ask questions with context
   response1 = agent.ask_question(session_id, "What is Python?")
   response2 = agent.ask_question(session_id, "What are its main features?")
   ```

### Example Implementation

```python
# Advanced usage example
from question_answering_agent.agent import QuestionAnsweringAgent

# Create an instance
agent = QuestionAnsweringAgent()

# Create a new session
session_id = agent.create_session("alice")

# Ask questions that build on each other
agent.ask_question(session_id, "I'm learning Python programming")
agent.ask_question(session_id, "What should I focus on first?")
agent.ask_question(session_id, "Can you recommend some resources?")

# Get session history
history = agent.get_session_history(session_id)
print(f"Conversation history: {history}")

# Update user preferences
agent.update_user_preferences(session_id, {
    "experience_level": "beginner",
    "learning_style": "hands-on"
})

# Ask context-aware question
response = agent.ask_question(session_id, "What's the best way to practice?")
```

## 🧠 Session Management

### Session Lifecycle
1. **Session Creation**: Initialize new conversation session
2. **Context Building**: Accumulate conversation context
3. **State Updates**: Update user preferences and session data
4. **Context Retrieval**: Access previous conversation context
5. **Session Cleanup**: Manage session expiration and cleanup

### State Management
- **User Preferences**: Store user-specific settings and preferences
- **Conversation History**: Maintain complete conversation log
- **Context Variables**: Store relevant context for future interactions
- **Session Metadata**: Track session creation time, last activity, etc.

## 🎯 Agent Capabilities

- **Contextual Responses**: Uses conversation history for better answers
- **Preference Learning**: Learns and adapts to user preferences
- **Multi-turn Conversations**: Handles complex, multi-turn dialogues
- **Session Persistence**: Maintains state across application restarts
- **Context Switching**: Can switch between different conversation topics
- **Memory Optimization**: Efficiently manages memory usage

## 📚 Learning Objectives

- Understanding session management in AI agents
- Implementing stateful conversation systems
- Working with conversation context and memory
- Building persistent user experiences
- Managing multi-user sessions
- Optimizing memory usage and performance

## 🔧 Technical Details

- **Language**: Python
- **Architecture**: Stateful session-based design
- **Storage**: In-memory and persistent storage options
- **Session ID**: Unique identifiers for session management
- **Context Window**: Configurable context length limits

## 💾 State Storage Options

### In-Memory Storage
```python
# Fast, temporary storage
session_data = {
    "session_id": "abc123",
    "user_id": "user456",
    "conversation_history": [...],
    "user_preferences": {...},
    "context": {...}
}
```

### Persistent Storage
```python
# Database or file-based storage
{
    "session_id": "abc123",
    "created_at": "2024-01-15T10:00:00Z",
    "last_activity": "2024-01-15T10:30:00Z",
    "data": {...}
}
```

## 🔄 Session Flow Example

```python
# 1. Create session
session_id = agent.create_session("user123")

# 2. Initial interaction
agent.ask_question(session_id, "Hi, I'm new to programming")

# 3. Context-aware follow-up
agent.ask_question(session_id, "What language should I start with?")

# 4. Update preferences based on conversation
agent.update_preferences(session_id, {"interests": ["web development"]})

# 5. Personalized recommendation
agent.ask_question(session_id, "What should I learn next?")
```

## 🎓 Next Steps

After mastering sessions and state, you can move on to:
- **5.Persistent-Storage**: Implement advanced data persistence
- **6.Multi-agent**: Build multi-agent systems with shared state