# 6. Multi-Agent Systems

This directory demonstrates how to build sophisticated multi-agent systems where multiple AI agents work together, communicate, and coordinate to solve complex problems.

## 📁 Contents

### Main Components
- `manager/` - Central agent manager and coordinator
  - `__init__.py` - Package initialization
  - `agent.py` - Main manager agent class
  - `sub_agents/` - Specialized sub-agents
    - `funny_nerd/` - Humorous technical agent
    - `joke_agent/` - Entertainment and humor agent
    - `stock_analyst/` - Financial analysis agent
  - `tools/` - Shared tools and utilities
    - `tools.py` - Common tools for all agents

### Additional Files
- `persistent_multi_agent.py` - Multi-agent system with persistent storage
- `state_management_tools.py` - Tools for managing agent state
- `print_latest_state.py` - Utility to display current system state
- `PERSISTENT_STORAGE_FLOW.md` - Documentation for persistent storage flow
- `README_PERSISTENT_STORAGE.md` - Detailed persistent storage documentation

## ✨ Features

- **Agent Coordination**: Multiple agents working together seamlessly
- **Specialized Roles**: Each agent has specific expertise and capabilities
- **Inter-Agent Communication**: Agents can communicate and share information
- **Task Distribution**: Intelligent task assignment and load balancing
- **Shared State Management**: Coordinated state across all agents
- **Persistent Multi-Agent**: Long-term memory and state persistence

## 🚀 Usage

### Quick Start

1. **Import the multi-agent system:**
   ```python
   from manager import agent
   ```

2. **Initialize and use the system:**
   ```python
   # Create the multi-agent system
   system = agent.MultiAgentSystem()
   
   # Process a complex request
   result = system.process_request("Tell me a funny joke about programming and then analyze Apple's stock")
   print(result)
   ```

### Example Implementation

```python
# Advanced usage example
from manager.agent import MultiAgentSystem

# Create an instance
system = MultiAgentSystem()

# Initialize with specific agents
system.add_agent("joke_agent", "entertainment")
system.add_agent("stock_analyst", "financial")
system.add_agent("funny_nerd", "technical_humor")

# Process complex multi-step requests
result = system.process_request("""
I need help with:
1. A programming joke to lighten the mood
2. Analysis of the current tech stock market
3. A funny explanation of machine learning concepts
""")

# Get individual agent responses
joke_response = system.get_agent_response("joke_agent")
stock_analysis = system.get_agent_response("stock_analyst")
tech_explanation = system.get_agent_response("funny_nerd")
```

## 🤖 Available Agents

### Manager Agent
- **Role**: Central coordinator and task distributor
- **Capabilities**: 
  - Task analysis and routing
  - Agent coordination
  - Response aggregation
  - System monitoring

### Sub-Agents

#### Funny Nerd Agent
- **Role**: Technical humor and programming jokes
- **Capabilities**:
  - Programming-related humor
  - Technical explanations with humor
  - Code jokes and puns
  - Developer-friendly content

#### Joke Agent
- **Role**: General entertainment and humor
- **Capabilities**:
  - General jokes and humor
  - Storytelling
  - Entertainment content
  - Mood lightening

#### Stock Analyst Agent
- **Role**: Financial analysis and market insights
- **Capabilities**:
  - Stock market analysis
  - Financial data interpretation
  - Investment insights
  - Market trend analysis

## 🎯 System Capabilities

- **Intelligent Routing**: Automatically routes tasks to appropriate agents
- **Parallel Processing**: Multiple agents can work simultaneously
- **Response Aggregation**: Combines responses from multiple agents
- **Context Sharing**: Agents share relevant context and information
- **Load Balancing**: Distributes workload efficiently across agents
- **Fault Tolerance**: System continues working even if some agents fail

## 📚 Learning Objectives

- Understanding multi-agent system architecture
- Implementing agent coordination and communication
- Building specialized agent roles and capabilities
- Managing shared state across multiple agents
- Implementing task distribution and load balancing
- Creating fault-tolerant multi-agent systems

## 🔧 Technical Details

- **Language**: Python
- **Architecture**: Distributed multi-agent system
- **Communication**: Inter-agent messaging and coordination
- **State Management**: Shared state with conflict resolution
- **Extensibility**: Easy to add new agents and capabilities

## 🔄 Multi-Agent Workflow

```python
# 1. Request Analysis
request = "Tell me a joke and analyze Tesla stock"
analysis = manager.analyze_request(request)

# 2. Task Distribution
tasks = manager.distribute_tasks(analysis)
# Result: [("joke_agent", "tell_joke"), ("stock_analyst", "analyze_stock")]

# 3. Parallel Execution
responses = manager.execute_tasks_parallel(tasks)

# 4. Response Aggregation
final_response = manager.aggregate_responses(responses)
```

## 🛠️ Agent Communication

### Message Types
- **Task Assignment**: Manager to sub-agents
- **Status Updates**: Sub-agents to manager
- **Data Sharing**: Between agents
- **Error Reporting**: Error handling and recovery

### Communication Protocol
```python
# Task assignment message
{
    "type": "task_assignment",
    "task_id": "task_123",
    "agent_id": "joke_agent",
    "payload": {
        "action": "tell_joke",
        "parameters": {"topic": "programming"}
    }
}

# Response message
{
    "type": "task_response",
    "task_id": "task_123",
    "agent_id": "joke_agent",
    "status": "completed",
    "result": "Why do programmers prefer dark mode? Because light attracts bugs!"
}
```

## 💾 Persistent Multi-Agent System

The system includes advanced persistent storage capabilities:

- **Agent State Persistence**: Each agent's state is saved
- **Conversation History**: Complete interaction history
- **Shared Knowledge Base**: Common knowledge accessible to all agents
- **Performance Metrics**: Track agent performance and usage
- **System Configuration**: Persistent system settings

## 🎓 Next Steps

After mastering multi-agent systems, you can:
- Extend the system with more specialized agents
- Implement advanced coordination algorithms
- Add machine learning for intelligent task routing
- Build domain-specific multi-agent applications
- Scale to larger, more complex systems
