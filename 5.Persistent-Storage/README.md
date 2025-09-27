# 5. Persistent Storage

This directory demonstrates how to implement persistent storage for AI agents, enabling data persistence across sessions, application restarts, and system reboots.

## 📁 Contents

### Agent Module
- `memory_agent/` - Agent with persistent storage capabilities
  - `__init__.py` - Package initialization file
  - `agent.py` - Main agent class with persistent memory

### Additional Files
- `main.py` - Main application entry point
- `utils.py` - Utility functions for storage operations

## ✨ Features

- **Persistent Memory**: Stores data that survives application restarts
- **Database Integration**: Works with various database systems
- **File-based Storage**: Supports JSON, CSV, and other file formats
- **Data Serialization**: Handles complex data structures
- **Backup and Recovery**: Includes data backup and recovery mechanisms
- **Query Capabilities**: Advanced querying and search functionality

## 🚀 Usage

### Quick Start

1. **Import the memory agent:**
   ```python
   from memory_agent import agent
   ```

2. **Create and use the agent:**
   ```python
   # Initialize the agent with persistent storage
   agent = agent.MemoryAgent(storage_type="database")
   
   # Store information
   agent.store_memory("user_preferences", {
       "name": "John",
       "preferred_language": "Python",
       "experience_level": "intermediate"
   })
   
   # Retrieve information
   preferences = agent.retrieve_memory("user_preferences")
   print(preferences)
   ```

### Example Implementation

```python
# Advanced usage example
from memory_agent.agent import MemoryAgent

# Create an instance with different storage options
agent = MemoryAgent(storage_type="sqlite", db_path="agent_memory.db")

# Store different types of data
agent.store_memory("conversation_history", {
    "session_id": "abc123",
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"}
    ],
    "timestamp": "2024-01-15T10:00:00Z"
})

agent.store_memory("user_learning_progress", {
    "user_id": "user456",
    "completed_topics": ["variables", "functions", "classes"],
    "current_topic": "inheritance",
    "progress_percentage": 75
})

# Query and search data
recent_conversations = agent.search_memory("conversation_history", 
                                         {"timestamp": {"$gte": "2024-01-01"}})

user_progress = agent.retrieve_memory("user_learning_progress", 
                                    {"user_id": "user456"})
```

## 💾 Storage Options

### Database Storage
- **SQLite**: Lightweight, file-based database
- **PostgreSQL**: Robust, feature-rich database
- **MySQL**: Popular relational database
- **MongoDB**: Document-based NoSQL database

### File-based Storage
- **JSON Files**: Human-readable, easy to work with
- **CSV Files**: Tabular data storage
- **Pickle Files**: Python object serialization
- **YAML Files**: Human-readable configuration format

## 🎯 Agent Capabilities

- **Data Persistence**: Ensures data survives application restarts
- **Advanced Queries**: Complex querying and filtering capabilities
- **Data Relationships**: Handles related data and references
- **Backup Management**: Automated backup and recovery
- **Data Migration**: Easy migration between storage systems
- **Performance Optimization**: Efficient data access and storage

## 📚 Learning Objectives

- Understanding persistent storage in AI agents
- Working with different database systems
- Implementing data serialization and deserialization
- Building robust data management systems
- Understanding data backup and recovery strategies
- Optimizing storage performance and efficiency

## 🔧 Technical Details

- **Language**: Python
- **Architecture**: Storage-agnostic design with pluggable backends
- **Dependencies**: Database drivers, serialization libraries
- **Extensibility**: Easy to add new storage backends
- **Performance**: Optimized for read/write operations

## 🗄️ Storage Schema Examples

### User Profile Schema
```json
{
  "user_id": "unique_user_id",
  "profile": {
    "name": "John Doe",
    "email": "john@example.com",
    "preferences": {
      "language": "Python",
      "theme": "dark",
      "notifications": true
    }
  },
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "last_updated": "2024-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

### Conversation Schema
```json
{
  "conversation_id": "conv_123",
  "user_id": "user_456",
  "messages": [
    {
      "message_id": "msg_001",
      "role": "user",
      "content": "Hello, how are you?",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "message_id": "msg_002",
      "role": "assistant",
      "content": "I'm doing well, thank you!",
      "timestamp": "2024-01-15T10:00:05Z"
    }
  ],
  "context": {
    "topic": "greeting",
    "sentiment": "positive"
  }
}
```

## 🔄 Data Operations

### Basic Operations
```python
# Store data
agent.store_memory("key", data)

# Retrieve data
data = agent.retrieve_memory("key")

# Update data
agent.update_memory("key", updated_data)

# Delete data
agent.delete_memory("key")
```

### Advanced Operations
```python
# Search with filters
results = agent.search_memory("collection", {"field": "value"})

# Batch operations
agent.batch_store([("key1", data1), ("key2", data2)])

# Backup data
agent.backup_data("backup_20240115.json")

# Restore data
agent.restore_data("backup_20240115.json")
```

## 🛡️ Data Security and Backup

- **Encryption**: Optional data encryption for sensitive information
- **Access Control**: User-based access permissions
- **Audit Logging**: Track all data access and modifications
- **Automated Backups**: Scheduled backup operations
- **Data Validation**: Ensure data integrity and consistency

## 🎓 Next Steps

After mastering persistent storage, you can move on to:
- **6.Multi-agent**: Build multi-agent systems with shared persistent storage