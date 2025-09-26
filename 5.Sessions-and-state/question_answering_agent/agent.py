from google.adk import Agent
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
import os
#---model--

load_dotenv('/home/arvind/AI-agents-Dev/.env', override=False)
model = LiteLlm(
    model="openrouter/deepseek/deepseek-chat-v3.1:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

question_answering_agent = Agent(
    name="question_answering_agent",
    model=model,
    description="Question answering agent",
    instruction ="""
    You are a helpful assistant that answers questions about the user's preferences.

    Here is some information about the user:
    Name:
    {user_name:Unknown User}
    Preferences:
    {user_preferences:No preferences provided}
    """,
)

root_agent = question_answering_agent

