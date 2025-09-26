# Sessions and State Agent

This directory demonstrates how to implement stateful agents that maintain context across conversations.

## Contents

### Main Files
- `basic_stateful_session.py` - Basic implementation of stateful sessions

### Agent Module
- `question_answering_agent/` - Stateful Q&A agent
  - `__init__.py` - Package initialization
  - `agent.py` - Agent class with session management

## Features

- **Session Management**: Maintains conversation state
- **Context Awareness**: Remembers previous interactions
- **State Persistence**: Keeps track of conversation history
- **Question Answering**: Specialized for Q&A scenarios

## Usage

1. Run the basic session example:
   ```bash
   python basic_stateful_session.py
   ```

2. Use the Q&A agent:
   ```python
   from question_answering_agent import agent
   
   # Create stateful agent
   qa_agent = agent.QuestionAnsweringAgent()
   
   # Ask questions with context
   response = qa_agent.ask("What is Python?")
   follow_up = qa_agent.ask("What are its main features?")
   ```

## Session Features

- **Conversation History**: Tracks all previous exchanges
- **Context Continuity**: Maintains context across questions
- **State Management**: Handles complex conversation flows
- **Memory**: Remembers user preferences and history

## Learning Objectives

- Understanding session management in AI agents
- Implementing stateful conversations
- Building context-aware systems
- Creating persistent user experiences
