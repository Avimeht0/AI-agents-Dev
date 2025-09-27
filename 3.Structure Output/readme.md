# 3. Structure Output

This directory demonstrates how to create AI agents that generate structured, well-formatted outputs for better user experience and data processing.

## 📁 Contents

### Agent Module
- `email_agent/` - Agent that generates structured email content
  - `__init__.py` - Package initialization file
  - `agent.py` - Main agent class with structured output capabilities

## ✨ Features

- **Structured Output Generation**: Creates well-formatted, consistent responses
- **Template-based Responses**: Uses templates for consistent formatting
- **Data Validation**: Ensures output follows predefined schemas
- **Multiple Output Formats**: Supports JSON, XML, HTML, and plain text
- **Custom Formatting**: Allows for custom output structures
- **Error Handling**: Graceful handling of formatting errors

## 🚀 Usage

### Quick Start

1. **Import the email agent:**
   ```python
   from email_agent import agent
   ```

2. **Create and use the agent:**
   ```python
   # Initialize the agent
   agent = agent.EmailAgent()
   
   # Generate structured email
   email_content = agent.generate_email(
       recipient="john@example.com",
       subject="Meeting Reminder",
       body="Don't forget about our meeting tomorrow at 2 PM."
   )
   print(email_content)
   ```

### Example Implementation

```python
# Advanced usage example
from email_agent.agent import EmailAgent

# Create an instance
agent = EmailAgent()

# Generate different types of structured emails
welcome_email = agent.generate_email(
    recipient="newuser@example.com",
    email_type="welcome",
    user_name="Alice",
    company="TechCorp"
)

meeting_email = agent.generate_email(
    recipient="team@example.com",
    email_type="meeting",
    meeting_date="2024-01-15",
    meeting_time="14:00",
    location="Conference Room A"
)

# Generate structured data
structured_data = agent.generate_structured_output(
    data_type="user_profile",
    data={
        "name": "John Doe",
        "email": "john@example.com",
        "role": "Developer"
    }
)
```

## 📧 Email Agent Capabilities

### Email Types
- **Welcome Emails**: Professional welcome messages for new users
- **Meeting Invitations**: Structured meeting requests with all details
- **Notifications**: System notifications and alerts
- **Reports**: Formatted reports and summaries
- **Follow-ups**: Professional follow-up communications

### Output Formats
- **HTML**: Rich HTML emails with styling
- **Plain Text**: Simple text-based emails
- **JSON**: Structured data for API responses
- **XML**: XML-formatted content
- **Markdown**: Markdown-formatted content

## 🎯 Agent Capabilities

- **Template Management**: Uses predefined templates for consistency
- **Dynamic Content**: Fills templates with dynamic data
- **Format Validation**: Ensures output follows specified formats
- **Multi-language Support**: Supports multiple languages
- **Custom Styling**: Applies custom CSS and formatting
- **Batch Processing**: Handles multiple emails efficiently

## 📚 Learning Objectives

- Understanding structured output generation in AI agents
- Implementing template-based response systems
- Working with different output formats (JSON, XML, HTML)
- Data validation and schema enforcement
- Template engine integration
- Professional email formatting and styling

## 🔧 Technical Details

- **Language**: Python
- **Architecture**: Template-based structured output
- **Dependencies**: Template engines, validation libraries
- **Extensibility**: Easy to add new output formats and templates
- **Validation**: Schema-based output validation

## 📋 Output Structure Examples

### Email Structure
```json
{
  "to": "recipient@example.com",
  "subject": "Email Subject",
  "body": {
    "html": "<html>...</html>",
    "text": "Plain text version"
  },
  "headers": {
    "from": "sender@example.com",
    "reply-to": "noreply@example.com"
  }
}
```

### User Profile Structure
```json
{
  "user_id": "12345",
  "profile": {
    "name": "John Doe",
    "email": "john@example.com",
    "role": "Developer",
    "department": "Engineering"
  },
  "metadata": {
    "created_at": "2024-01-01T00:00:00Z",
    "last_updated": "2024-01-15T10:30:00Z"
  }
}
```

## 🎓 Next Steps

After mastering structured output, you can move on to:
- **4.Sessions-and-state**: Add memory and conversation state
- **5.Persistent-Storage**: Implement data persistence
- **6.Multi-agent**: Build multi-agent systems