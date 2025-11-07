# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI Key ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Reddit Keys ---
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

PROJECT_NAME = "InsightEngine"
API_V1_STR = "/api/v1"
