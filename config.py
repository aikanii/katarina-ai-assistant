"""
Central configuration for Katarina.
All secrets are read from environment variables — never hardcode keys here.

Get a free Gemini API key at: https://aistudio.google.com/apikey

Put your key in a ".env" file in this folder (see .env.example):
    GEMINI_API_KEY=AIza...

".env" is in .gitignore, so it's never committed to version control.
"""
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env into the environment, if present

# --- LLM brain ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL = "gemini-flash-latest"         # always points at Google's current recommended Flash model
MAX_TOKENS = 1024

# --- Assistant identity ---
ASSISTANT_NAME = "Katarina"
WAKE_WORD = "katarina"                # said at the start of a typed/spoken command (optional, see main.py)

# --- Voice I/O ---
VOICE_ENABLED = True                  # set False to run in text-only mode
TTS_RATE = 185                        # words per minute for text-to-speech
TTS_VOLUME = 1.0
MIC_TIMEOUT = 6                       # seconds to wait for speech to start
MIC_PHRASE_LIMIT = 12                 # max seconds for a single phrase

# --- Personality (system prompt for the brain) ---
SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, a concise, capable personal AI assistant \
running locally on the user's computer, inspired by JARVIS from Iron Man. \
Keep spoken responses SHORT (1-3 sentences) since they will be read aloud by text-to-speech, \
unless the user explicitly asks for detail. Be dry-witted but genuinely helpful. \
You cannot control the operating system yourself — if the user wants an action performed \
(opening an app, searching the web, checking the time, adjusting volume), say so plainly; \
the skills system, not you, will have already tried to handle those before your turn.
"""
