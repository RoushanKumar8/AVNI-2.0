import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

WAKE_PHRASES = [
    "hey avni",
    "hi avni",
    "hii avni",
    "avni",
    "hello avni",
    "helo avni",
]

SYSTEM_PROMPT = """
You are Avni, an English-only desktop AI assistant.

Rules:
1. Communicate only in English.
2. Keep responses concise and natural for voice.
3. Do not respond in Hindi.
4. Do not pretend that you performed an action unless the program actually did it.
"""