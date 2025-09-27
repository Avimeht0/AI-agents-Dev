import os
import random
from dotenv import load_dotenv

from google.adk.models.lite_llm import LiteLlm
from google.adk import Agent

# Load environment variables from root .env
load_dotenv('/home/arvind/AI-agents-Dev/.env', override=False)

# Define the tool function
def bad_jokes() -> str:
    jokes_list = [
        "Why don’t skeletons fight each other? - They don’t have the guts.",
        "I’m reading a book about anti-gravity. It’s impossible to put down.",
        "Why did the scarecrow win an award? - Because he was outstanding in his field!",
        "What’s orange and sounds like a parrot? - A carrot.",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "Why don’t programmers like nature? - It has too many bugs.",
        "I told my computer I needed a break. - Now it won’t stop sending me Kit-Kats.",
        "Why was the math book sad? - Because it had too many problems.",
        "What do you call fake spaghetti? - An impasta."
    ]
    return random.choice(jokes_list)

# Model setup
model = LiteLlm(
    model="openrouter/deepseek/deepseek-chat-v3.1:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Agent definition (just pass the function directly)
root_agent = Agent(
    name="tool_agent",
    model=model,
    description="Tool agent that tells jokes",
    instruction="""
    You are a helpful assistant that can use the following tool:
    - bad_jokes: returns a random joke.
    When someone asks for a joke, always call the tool and print the result directly.
    """,
    tools=[bad_jokes],  # ✅ Pass the function directly
)

