from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent=Agent(
    name="greeting_agent",
    model=LiteLlm(model="gpt-4o-mini"),
    description="A greeting agent that greets the user",
    instruction="You are a greeting agent that greets the user",
     
)