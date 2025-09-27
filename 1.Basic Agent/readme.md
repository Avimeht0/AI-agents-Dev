# 1. Basic Agent

This directory contains a simple greeting agent implementation that demonstrates the fundamental concepts of AI agent development.

## 📁 Contents

### Agent Module
- `greeting_agent/` - Basic agent implementation
  - `__init__.py` - Package initialization file
  - `agent.py` - Main agent class with greeting functionality

## ✨ Features

- **Simple Greeting**: Basic agent that can greet users with personalized messages
- **Modular Design**: Clean separation of concerns with well-structured code
- **Easy to Extend**: Foundation for building more complex agents
- **Basic Conversation**: Handles simple user interactions

## 🚀 Usage

### Quick Start

1. **Import the agent:**
   ```python
   from greeting_agent import agent
   ```

2. **Create and use the agent:**
   ```python
   # Initialize the agent
   my_agent = agent.GreetingAgent()
   
   # Use the agent to greet someone
   response = my_agent.greet("John")
   print(response)  # Output: "Hello, John! Nice to meet you!"
   ```

### Example Implementation

```python
# Basic usage example
from greeting_agent.agent import GreetingAgent

# Create an instance
agent = GreetingAgent()

# Greet a user
greeting = agent.greet("Alice")
print(greeting)

# Handle different types of greetings
formal_greeting = agent.greet("Dr. Smith", formal=True)
casual_greeting = agent.greet("Bob", formal=False)
```

## 🎯 Agent Capabilities

- **Personalized Greetings**: Creates custom greetings based on user input
- **Basic Conversation Handling**: Processes simple user interactions
- **Simple Response Generation**: Generates appropriate responses
- **Formal/Casual Modes**: Supports different greeting styles

## 📚 Learning Objectives

- Understanding basic agent architecture and design patterns
- Implementing simple AI agent patterns from scratch
- Learning modular code organization for agents
- Foundation for more advanced agent development
- Introduction to agent-user interaction patterns

## 🔧 Technical Details

- **Language**: Python
- **Architecture**: Object-oriented design
- **Dependencies**: Minimal external dependencies
- **Extensibility**: Easy to add new greeting types and features

## 🎓 Next Steps

After mastering this basic agent, you can move on to:
- **2.Tools**: Learn how to integrate external tools
- **3.Structure Output**: Understand structured response generation
- **4.Sessions-and-state**: Add memory and conversation state
