from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm
import os
#---Model---
load_dotenv('/home/arvind/AI-agents-Dev/.env', override=False)
model = LiteLlm(
    model="openrouter/deepseek/deepseek-chat-v3.1:free",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


#---Define output schema---

class EmailContent(BaseModel):
    subject:str =Field(
        description="The subject line of the email. Should be concise and descriptive"

    )
    body:str=Field(
        descrption="The main content of the email.should be well-formatted with proper greeting , paragraphs, and signature "
        )
    

#--- Create Email Generator Agent ---
root_agent=LlmAgent(
    name="email_agent",
    model=model,
    instruction="""
    You are an Email Generation Assistant.
    Your task is to generate a professional email based on the user's request.

    GUIDELINES:
    -Create an appropriate subject line (concise and relevant)
    -Write a well-structured email body with:
        * Professional greeting 
        * Clear and consise main content 
        * Appropriate closing
        * Your name as signature
    - Suggest relevant attachments if applicable (empty list if none needed)
    - Email tone should match the purpose (formal for business, friendly for colleagues)
    - Keep emails concise but complete

    IMPORTANT: Your response MUST be valic JSON matching this structure
    {
    "subject": "Subject line here",
    "body": "Email body here with proper paragraphs and formatting",
    }

    DO NoT include any explanations or additional text outside the JSON response.

    """,
    description="Generates professional emails with structured subject and body",
    output_schema=EmailContent,
    output_key="email",

)