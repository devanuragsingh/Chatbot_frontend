# Hinglish: Ye FastAPI ka main entry point hai

from dotenv import load_dotenv
import os

load_dotenv()  # ✅ Load .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ NEW
from app.routes.chat import router as chat_router
from app.core.database import create_table

app = FastAPI()

# 🧠 Database initialize kar rahe hain
create_table()

# 🌐 CORS enable (frontend connect karne ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # sabko allow kar rahe hain (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔗 Routes connect kar rahe hain
app.include_router(chat_router)

@app.get("/")
def home():
    return {"message": "AI Chatbot Running 🚀"}