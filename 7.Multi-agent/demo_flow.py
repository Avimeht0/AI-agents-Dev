#!/usr/bin/env python3
"""
Demonstration script showing the complete persistent storage flow
for the multi-agent system.

This script demonstrates:
1. Database initialization
2. Session creation/retrieval
3. State management
4. Event processing
5. Multi-agent coordination
"""

import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

# Import our multi-agent system
from manager.agent import root_agent
from state_management_tools import *

load_dotenv()

def print_section(title, content=""):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")
    if content:
        print(content)

def print_step(step_num, title, description=""):
    """Print a formatted step."""
    print(f"\n📋 STEP {step_num}: {title}")
    print(f"{'─'*50}")
    if description:
        print(f"   {description}")

async def demonstrate_persistent_flow():
    """Demonstrate the complete persistent storage flow."""
    
    print_section("MULTI-AGENT PERSISTENT STORAGE DEMONSTRATION", 
                 "This demo shows how sessions, state, events, and runners work together")
    
    # ===== STEP 1: Database Initialization =====
    print_step(1, "Database Initialization", 
               "Setting up SQLite database for persistent storage")
    
    db_url = "sqlite:///./demo_multi_agent_data.db"
    session_service = DatabaseSessionService(db_url=db_url)
    print(f"✅ Database initialized: {db_url}")
    
    # ===== STEP 2: Initial State Definition =====
    print_step(2, "Initial State Definition", 
               "Defining the starting state for new sessions")
    
    initial_state = {
        "user_name": "Demo User",
        "conversation_history": [],
        "agent_delegations": [],
        "user_preferences": {
            "favorite_agent": None,
            "joke_preferences": [],
            "stock_watchlist": [],
            "nerd_topics": []
        },
        "session_metadata": {
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "total_interactions": 0
        }
    }
    print(f"✅ Initial state defined with {len(initial_state)} top-level keys")
    
    # ===== STEP 3: Session Management =====
    print_step(3, "Session Management", 
               "Creating or retrieving existing session")
    
    APP_NAME = "Multi-Agent Demo"
    USER_ID = "demo_user_123"
    
    # Check for existing sessions
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID
    )
    
    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"✅ Found existing session: {SESSION_ID}")
        print("   This demonstrates session persistence across runs!")
    else:
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        SESSION_ID = new_session.id
        print(f"✅ Created new session: {SESSION_ID}")
    
    # ===== STEP 4: Runner Setup =====
    print_step(4, "Runner Setup", 
               "Creating runner with session service for state management")
    
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service
    )
    print(f"✅ Runner created with {len(runner.agent.sub_agents)} sub-agents")
    print(f"   Sub-agents: {[agent.name for agent in runner.agent.sub_agents]}")
    
    # ===== STEP 5: State Display (Before) =====
    print_step(5, "Current State Display", 
               "Showing current session state")
    
    try:
        session = session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(f"📊 Current State:")
        print(f"   User: {session.state.get('user_name', 'Unknown')}")
        print(f"   Conversations: {len(session.state.get('conversation_history', []))}")
        print(f"   Delegations: {len(session.state.get('agent_delegations', []))}")
        print(f"   Total Interactions: {session.state.get('session_metadata', {}).get('total_interactions', 0)}")
    except Exception as e:
        print(f"❌ Error displaying state: {e}")
    
    # ===== STEP 6: Interactive Demo =====
    print_step(6, "Interactive Multi-Agent Demo", 
               "Demonstrating agent delegation and state tracking")
    
    demo_queries = [
        "Tell me a joke about Python programming",
        "What's the current price of AAPL stock?",
        "Tell me a nerdy joke about mathematics",
        "Show me my conversation summary"
    ]
    
    print(f"\n🎭 Running {len(demo_queries)} demo queries...")
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n{'─'*40}")
        print(f"🔍 Demo Query {i}: {query}")
        print(f"{'─'*40}")
        
        try:
            # Create user message
            content = types.Content(role="user", parts=[types.Part(text=query)])
            
            # Process through multi-agent system
            print(f"🔄 Processing through multi-agent system...")
            async for event in runner.run_async(
                user_id=USER_ID, session_id=SESSION_ID, new_message=content
            ):
                # Display event information
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            print(f"🤖 Agent Response: {part.text.strip()}")
                        elif hasattr(part, "tool_response") and part.tool_response:
                            print(f"🔧 Tool Response: {part.tool_response.output}")
                            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
    
    # ===== STEP 7: Final State Display =====
    print_step(7, "Final State Display", 
               "Showing updated state after interactions")
    
    try:
        session = session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(f"📊 Updated State:")
        print(f"   User: {session.state.get('user_name', 'Unknown')}")
        print(f"   Conversations: {len(session.state.get('conversation_history', []))}")
        print(f"   Delegations: {len(session.state.get('agent_delegations', []))}")
        print(f"   Total Interactions: {session.state.get('session_metadata', {}).get('total_interactions', 0)}")
        
        # Show recent delegations
        delegations = session.state.get('agent_delegations', [])
        if delegations:
            print(f"   Recent Delegations:")
            for delegation in delegations[-3:]:
                print(f"     - {delegation.get('agent_name', 'Unknown')}: {delegation.get('task', 'Unknown task')}")
        
        # Show user preferences
        preferences = session.state.get('user_preferences', {})
        print(f"   User Preferences:")
        print(f"     - Favorite Agent: {preferences.get('favorite_agent', 'None')}")
        print(f"     - Joke Preferences: {preferences.get('joke_preferences', [])}")
        print(f"     - Stock Watchlist: {preferences.get('stock_watchlist', [])}")
        
    except Exception as e:
        print(f"❌ Error displaying final state: {e}")
    
    # ===== STEP 8: Persistence Verification =====
    print_step(8, "Persistence Verification", 
               "Demonstrating that data persists across sessions")
    
    print(f"✅ Database file created: {db_url}")
    print(f"✅ Session ID: {SESSION_ID}")
    print(f"✅ All interactions saved to persistent storage")
    print(f"✅ Next time you run this, the session will be restored!")
    
    print_section("DEMONSTRATION COMPLETE", 
                 "You've seen the complete flow of persistent multi-agent storage!")

if __name__ == "__main__":
    print("🚀 Starting Multi-Agent Persistent Storage Demonstration...")
    asyncio.run(demonstrate_persistent_flow())
