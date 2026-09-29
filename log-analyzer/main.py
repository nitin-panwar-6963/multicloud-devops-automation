from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated
from openai import OpenAI
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage


# Load environment variables
load_dotenv()


# Email credentials
sender_email = os.environ.get("SENDER_EMAIL")
receiver_email = os.environ.get("RECEIVER_EMAIL")
app_password = os.environ.get("APP_PASSWORD")


def mail_sender(source, content):
    msg = EmailMessage()
    msg["Subject"] = source
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    return f"Email is Send to {receiver_email}"


# FastAPI object
app = FastAPI(
    title="Nitin Log Analyzer 🚀",
    description="AI-powered Log Analyzer for Developers and DevOps Engineers",
    version="1.0.0"
)


# Groq client
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# Pydantic model
class LogRequest(BaseModel):
    logs: Annotated[
        str,
        Field(
            strict=True,
            description="Jenkins or GitHub Actions pipeline logs"
        )
    ]


SYSTEM_PROMPT = """You are Nitin Log Analyzer, a CI/CD failure analysis assistant.

Analyze the provided Jenkins or GitHub Actions pipeline logs.

Identify:
1. Failed stage/job
2. Actual error
3. Root cause
4. Exactly 3 practical solutions

Return ONLY the following format:

🚨 Pipeline Failure

🔵 Platform: [Jenkins/GitHub Actions]

📍 Failed Stage:
[stage/job]

❌ Error:
[actual error]

🔎 Root Cause:
[clear explanation]

💡 Solutions:

1. [Solution title]
[short practical solution]

2. [Solution title]
[short practical solution]

3. [Solution title]
[short practical solution]

🛠️ Recommended Action:
[what should be checked/fixed first]

Rules:
- Analyze only the provided logs.
- Do not hallucinate.
- Focus on the first meaningful failure.
- Keep the response concise and email-friendly.
- Always provide exactly 3 solutions."""


# Main route
@app.get("/")
def greet():
    return {
        "message": "🚀 Nitin Log Analyzer API is working!",
        "status": "online",
        "version": "1.0.0"
    }


# Webhook route
@app.post("/webhook/{platform}")
def analyze_logs(
    platform: str,
    request: LogRequest
):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
Pipeline Platform:
{platform}

Logs to Analyze:

{request.logs}
"""
            }
        ]
    )

    # Get AI response
    analysis = response.choices[0].message.content

    # Return response
    return {
        "Email_status": mail_sender(
            f"{platform} Pipeline Failue Analysis",
            analysis
        )
    }