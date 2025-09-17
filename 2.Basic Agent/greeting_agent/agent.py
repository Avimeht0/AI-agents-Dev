from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
load_dotenv()
model = LiteLlm(model="openrouter/mistralai/mistral-small-3.2-24b-instruct:free",
               api_key=os.getenv("OPENROUTER_API_KEY"))



root_agent=Agent(
    name="greeting_agent",
    model=model,
    description="A greeting agent that greets the user",
    instruction="You are a greeting agent that greets the user",
     
)