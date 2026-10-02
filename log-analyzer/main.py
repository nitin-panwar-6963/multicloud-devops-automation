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

# Email Configuration

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

        smtp.login(
            sender_email,
            app_password
        )

        smtp.send_message(msg)

    return f"Email is sent to {receiver_email}"

# FastAPI Application
app = FastAPI(
    title="Nitin Log Analyzer 🚀",
    description="AI-powered Log Analyzer for Developers and DevOps Engineers",
    version="1.0.0"
)

# Groq Client
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)
# Pydantic Model
class LogRequest(BaseModel):

    logs: Annotated[
        str,
        Field(
            strict=True,
            description="Jenkins or GitHub Actions pipeline logs"
        )
    ]
# AI System Prompt

SYSTEM_PROMPT = """
You are Nitin Log Analyzer, a CI/CD failure analysis assistant.

Analyze the provided Jenkins or GitHub Actions pipeline logs.

Your main goal is to identify the ACTUAL reason why the pipeline failed.

IMPORTANT RULES:

1. Identify the error that actually TERMINATED the pipeline.

2. Give highest priority to actual Jenkins/Groovy/runtime errors such as:
   - MissingPropertyException
   - Compilation errors
   - Syntax errors
   - NullPointerException
   - Permission errors
   - Authentication errors
   - Command execution failures
   - Docker build failures
   - Docker push failures

3. Do NOT automatically treat warnings, informational messages,
   or vulnerability findings as the root cause.

4. Trivy vulnerabilities are NOT automatically the root cause.

5. If Trivy reports vulnerabilities but Jenkins later shows another
   terminating error, report the terminating Jenkins error.

6. For example, if the logs contain:

   MissingPropertyException:
   No such property: IMAGE_FRONTEN

   and the Jenkinsfile defines:

   IMAGE_FRONTEND

   then the actual error MUST be reported as:

   IMAGE_FRONTEN

7. Always use the exact error, variable name, command,
   and stage shown in the logs.

8. Do NOT modify or guess the error.

9. Do NOT invent information that is not present in the logs.

10. If multiple errors exist, determine which error actually
    caused Jenkins to terminate.

11. Distinguish between:
    - warnings
    - informational messages
    - vulnerability findings
    - actual pipeline failure

12. Always provide exactly 3 practical solutions.

Return ONLY the following format:

🚨 Pipeline Failure

🔵 Platform: [Jenkins/GitHub Actions]

📍 Failed Stage:
[actual failed stage]

❌ Error:
[exact actual error from the logs]

🔎 Root Cause:
[clear explanation based only on the logs]

💡 Solutions:

1. [Solution title]
[short practical solution]

2. [Solution title]
[short practical solution]

3. [Solution title]
[short practical solution]

🛠️ Recommended Action:
[the first thing that should be fixed]

Rules:

- Analyze only the provided logs.
- Do not hallucinate.
- Focus on the actual terminating error.
- Do not automatically blame Trivy.
- Keep the response concise and email-friendly.
- Always provide exactly 3 solutions.
"""

@app.get("/")
def greet():

    return {
        "message": "🚀 Nitin Log Analyzer API is working!",
        "status": "online",
        "version": "1.0.0"
    }
# Webhook Route
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


    # Send AI analysis through email
    email_status = mail_sender(
        f"{platform} Pipeline Failure Analysis",
        analysis
    )


    # Return response
    return {
        "Email_status": email_status
    }
