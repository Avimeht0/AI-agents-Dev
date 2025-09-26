# Structure Output Agent

This directory contains an agent that can generate structured outputs like emails, reports, and formatted documents.

## Contents

### Agent Module
- `email_agent/` - Agent for structured output generation
  - `__init__.py` - Package initialization
  - `agent.py` - Agent class with structured output capabilities

## Features

- **Structured Output**: Generates well-formatted documents
- **Email Generation**: Creates professional emails
- **Template System**: Uses templates for consistent formatting
- **Multiple Formats**: Supports various output structures

## Usage

1. Import the email agent:
   ```python
   from email_agent import agent
   ```

2. Generate structured content:
   ```python
   # Create the agent
   email_agent = agent.EmailAgent()
   
   # Generate structured email
   email = email_agent.generate_email(
       recipient="john@example.com",
       subject="Meeting Reminder",
       content="Don't forget our meeting tomorrow at 2 PM"
   )
   ```

## Output Types

- **Emails**: Professional email formatting
- **Reports**: Structured report generation
- **Documents**: Formatted document creation
- **Templates**: Reusable content templates

## Learning Objectives

- Understanding structured output generation
- Implementing template systems
- Creating professional document formats
- Building agents for content generation
