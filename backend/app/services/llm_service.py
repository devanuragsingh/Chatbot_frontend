import os
import requests
from dotenv import load_dotenv, find_dotenv

from app.services.memory import get_memory, add_message
from app.services.local_ai import local_response

# 🔍 Try to auto-find .env first
env_file = find_dotenv()

if env_file:
    print("📄 .env FOUND AT:", env_file)
    load_dotenv(env_file)
else:
    print("⚠️ .env NOT FOUND via find_dotenv, trying manual path...")
    load_dotenv("backend/.env")  # fallback

API_KEY = os.getenv("OPENROUTER_API_KEY")

print("🔑 API KEY VALUE:", API_KEY)


def generate_response(user_input, session_id):

    # Save user message
    add_message(session_id, "user", user_input)

    memory = get_memory(session_id)

    try:
        if not API_KEY:
            raise Exception("API KEY NOT FOUND")

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "AI Chatbot"
            },
            json={
                "model": "openrouter/auto",
                "messages": memory
            }
        )

        print("📡 STATUS:", response.status_code)
        print("📡 RESPONSE:", response.text)

        if response.status_code != 200:
            raise Exception(f"API ERROR: {response.text}")

        data = response.json()

        bot_reply = data.get("choices", [{}])[0].get("message", {}).get("content")

        if not bot_reply:
            raise Exception("EMPTY RESPONSE FROM MODEL")

    except Exception as e:
        print("❌ ERROR:", str(e))
        bot_reply = local_response(user_input, memory)

    # Save bot reply
    add_message(session_id, "assistant", bot_reply)

    return bot_reply