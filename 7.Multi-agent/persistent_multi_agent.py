import asyncio
from datetime import datetime
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

# Import the multi-agent manager
from manager.agent import root_agent
from utils import call_agent_async, display_state, Colors

load_dotenv()

# ===== PART 1: Initialize Persistent Session Service =====
# Using SQLite database for persistent storage
db_url = "sqlite:///./multi_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)

# ===== PART 2: Define Initial State for Multi-Agent System =====
# This will only be used when creating a new session
initial_state = {
    "user_name": "Arvind Mehta",
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

def display_multi_agent_state(session_service, app_name, user_id, session_id, label="Multi-Agent State"):
    """Display the current multi-agent session state in a formatted way."""
    try:
        session = session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )

        # Format the output with clear sections
        print(f"\n{'-' * 15} {label} {'-' * 15}")

        # Handle the user name
        user_name = session.state.get("user_name", "Unknown")
        print(f"👤 User: {user_name}")

        # Handle conversation history
        conversation_history = session.state.get("conversation_history", [])
        if conversation_history:
            print(f"💬 Conversation History: {len(conversation_history)} entries")
            # Show last 3 conversations
            for i, conv in enumerate(conversation_history[-3:], 1):
                print(f"  {i}. {conv.get('timestamp', 'Unknown time')}: {conv.get('user_input', '')[:50]}...")
        else:
            print("💬 Conversation History: None")

        # Handle agent delegations
        delegations = session.state.get("agent_delegations", [])
        if delegations:
            print(f"🤖 Agent Delegations: {len(delegations)} total")
            # Show recent delegations
            for i, delegation in enumerate(delegations[-3:], 1):
                print(f"  {i}. {delegation.get('timestamp', 'Unknown time')}: {delegation.get('agent_name', 'Unknown')} - {delegation.get('task', '')[:50]}...")
        else:
            print("🤖 Agent Delegations: None")

        # Handle user preferences
        preferences = session.state.get("user_preferences", {})
        print(f"⚙️  User Preferences:")
        print(f"  - Favorite Agent: {preferences.get('favorite_agent', 'None')}")
        print(f"  - Joke Preferences: {preferences.get('joke_preferences', [])}")
        print(f"  - Stock Watchlist: {preferences.get('stock_watchlist', [])}")
        print(f"  - Nerd Topics: {preferences.get('nerd_topics', [])}")

        # Handle session metadata
        metadata = session.state.get("session_metadata", {})
        print(f"📊 Session Metadata:")
        print(f"  - Created: {metadata.get('created_at', 'Unknown')}")
        print(f"  - Last Activity: {metadata.get('last_activity', 'Unknown')}")
        print(f"  - Total Interactions: {metadata.get('total_interactions', 0)}")

        print("-" * (30 + len(label)))
    except Exception as e:
        print(f"Error displaying multi-agent state: {e}")

async def process_multi_agent_response(event, session_service, app_name, user_id, session_id):
    """Process and display multi-agent response events with state tracking."""
    # Log basic event info
    print(f"Event ID: {event.id}, Author: {event.author}")

    # Check for specific parts first
    has_specific_part = False
    if event.content and event.content.parts:
        for part in event.content.parts:
            if hasattr(part, "executable_code") and part.executable_code:
                print(f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```")
                has_specific_part = True
            elif hasattr(part, "code_execution_result") and part.code_execution_result:
                print(f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}")
                has_specific_part = True
            elif hasattr(part, "tool_response") and part.tool_response:
                print(f"  Tool Response: {part.tool_response.output}")
                has_specific_part = True
            elif hasattr(part, "text") and part.text and not part.text.isspace():
                print(f"  Text: '{part.text.strip()}'")

    # Check for final response after specific parts
    final_response = None
    if event.is_final_response():
        if (event.content and event.content.parts and 
            hasattr(event.content.parts[0], "text") and event.content.parts[0].text):
            final_response = event.content.parts[0].text.strip()
            
            # Update session state with conversation history
            try:
                session = session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
                current_state = session.state
                
                # Add to conversation history
                conversation_history = current_state.get("conversation_history", [])
                conversation_history.append({
                    "timestamp": datetime.now().isoformat(),
                    "user_input": "User input from previous interaction",
                    "agent_response": final_response,
                    "event_id": event.id
                })
                current_state["conversation_history"] = conversation_history
                
                # Update session metadata
                metadata = current_state.get("session_metadata", {})
                metadata["last_activity"] = datetime.now().isoformat()
                metadata["total_interactions"] = metadata.get("total_interactions", 0) + 1
                current_state["session_metadata"] = metadata
                
                # Update the session
                session_service.update_session(
                    app_name=app_name,
                    user_id=user_id,
                    session_id=session_id,
                    state=current_state
                )
                
            except Exception as e:
                print(f"Error updating session state: {e}")
            
            # Display the response with formatting
            print(f"\n{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╔══ MULTI-AGENT RESPONSE ═════════════════════════════════════════{Colors.RESET}")
            print(f"{Colors.CYAN}{Colors.BOLD}{final_response}{Colors.RESET}")
            print(f"{Colors.BG_BLUE}{Colors.WHITE}{Colors.BOLD}╚═════════════════════════════════════════════════════════════{Colors.RESET}\n")
        else:
            print(f"\n{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD}==> Final Multi-Agent Response: [No text content in final event]{Colors.RESET}\n")

    return final_response

async def call_multi_agent_async(runner, user_id, session_id, query):
    """Call the multi-agent system asynchronously with the user's query."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"\n{Colors.BG_GREEN}{Colors.BLACK}{Colors.BOLD}--- Running Multi-Agent Query: {query} ---{Colors.RESET}")
    final_response_text = None

    # Display state before processing
    display_multi_agent_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State BEFORE processing",
    )

    try:
        async for event in runner.run_async(
            user_id=user_id, session_id=session_id, new_message=content
        ):
            # Process each event and get the final response if available
            response = await process_multi_agent_response(
                event, runner.session_service, runner.app_name, user_id, session_id
            )
            if response:
                final_response_text = response
    except Exception as e:
        print(f"Error during multi-agent call: {e}")

    # Display state after processing the message
    display_multi_agent_state(
        runner.session_service,
        runner.app_name,
        user_id,
        session_id,
        "State AFTER processing",
    )

    return final_response_text

async def main_async():
    # Setup constants
    APP_NAME = "Multi-Agent System"
    USER_ID = "arvind_rajesh_mehta"

    # ===== PART 3: Session Management - Find or Create =====
    # Check for existing sessions for this user
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # If there's an existing session, use it, otherwise create a new one
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # Use the most recent session
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing existing multi-agent session: {SESSION_ID}")
    else:
        # Create a new session with initial state
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"Created new multi-agent session: {SESSION_ID}")

    # ===== PART 4: Multi-Agent Runner Setup =====
    # Create a runner with the multi-agent manager
    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== PART 5: Interactive Multi-Agent Conversation Loop =====
    print("\n" + "="*60)
    print("🤖 WELCOME TO PERSISTENT MULTI-AGENT SYSTEM! 🤖")
    print("="*60)
    print("This system demonstrates how sessions, state, events, and runners work together:")
    print("1. 📊 Database Storage: SQLite database stores all session data")
    print("2. 🔄 Session Management: Find existing or create new sessions")
    print("3. 🏗️  Initial State: Define starting state for new sessions")
    print("4. 🏃 Runner: Orchestrates agent execution with session service")
    print("5. 📝 Events: Track agent responses and state changes")
    print("6. 💾 State Persistence: All interactions are saved automatically")
    print("\nAvailable Agents:")
    print("  - Manager Agent: Coordinates all other agents")
    print("  - Stock Analyst: Fetches stock prices")
    print("  - Funny Nerd: Tells nerdy jokes")
    print("  - Joke Agent: Tells general jokes")
    print("\nType 'exit' or 'quit' to end the conversation.")
    print("="*60)

    while True:
        # Get user input
        user_input = input("\nYou: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("\n" + "="*60)
            print("👋 Ending multi-agent conversation.")
            print("📊 All your data has been saved to the database.")
            print("🔄 Next time you run this, your conversation history will be preserved!")
            print("="*60)
            break

        # Process the user query through the multi-agent system
        await call_multi_agent_async(runner, USER_ID, SESSION_ID, user_input)

if __name__ == "__main__":
    asyncio.run(main_async())
