
import openai
import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Plugin system (we’ll expand this)
from fiads_plugins.email_plugin import fetch_latest_emails
from fiads_plugins.calendar_plugin import get_upcoming_events
from fiads_plugins.drive_plugin import list_drive_files
from fiads_plugins.news_plugin import fetch_news

def call_gpt4(prompt: str, context: str = "") -> str:
    """
    Sends prompt to OpenAI and returns the response.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"[FIADS Error] {str(e)}"

def fiads_router(user_input: str) -> str:
    """
    Routes the user's input to the appropriate plugin or GPT-4.
    """
    # Simple keyword-based routing (can upgrade to LLM routing later)
    if "email" in user_input.lower():
        emails = fetch_latest_emails()
        return "Here are your latest emails:\n\n" + "\n\n".join(emails)

    elif "calendar" in user_input.lower() or "schedule" in user_input.lower():
        events = get_upcoming_events()
        return "Here are your upcoming events:\n\n" + "\n\n".join(events)

    elif "drive" in user_input.lower() or "file" in user_input.lower():
        files = list_drive_files()
        return "Here are recent files from Drive:\n\n" + "\n\n".join(files)

    elif "news" in user_input.lower():
        headlines = fetch_news()
        return "Today’s top news:\n\n" + "\n\n".join(headlines)

    else:
        # Fall back to GPT-4
        return call_gpt4(user_input, context="You are FIADS, a helpful and secure AI assistant.")
