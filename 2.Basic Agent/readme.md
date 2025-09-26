# Basic Agent

This directory contains a simple greeting agent implementation.

## Contents

### Agent Module
- `greeting_agent/` - Basic agent implementation
  - `__init__.py` - Package initialization
  - `agent.py` - Main agent class with greeting functionality

## Features

- **Simple Greeting**: Basic agent that can greet users
- **Modular Design**: Clean separation of concerns
- **Easy to Extend**: Foundation for more complex agents

## Usage

1. Import the agent:
   ```python
   from greeting_agent import agent
   ```

2. Create and use the agent:
   ```python
   # Initialize the agent
   my_agent = agent.GreetingAgent()
   
   # Use the agent
   response = my_agent.greet("John")
   print(response)
   ```

## Agent Capabilities

- Personalized greetings
- Basic conversation handling
- Simple response generation

## Learning Objectives

- Understanding basic agent architecture
- Implementing simple AI agent patterns
- Foundation for more advanced agent development
