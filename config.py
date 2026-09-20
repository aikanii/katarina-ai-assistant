"""Configuration loaded from environment variables (and an optional .env file)."""
import os
from dotenv import load_dotenv

load_dotenv()


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


_raw_key = os.getenv("GEMINI_API_KEY", "").strip()
# Treat the example placeholder as unset so first-run setup stays offline.
GEMINI_API_KEY = "" if _raw_key in {"", "your-key-here", "your_api_key_here"} else _raw_key
MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", "1024"))
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "Katarina")
VOICE_ENABLED = _bool_env("VOICE_ENABLED", True)
TTS_RATE = int(os.getenv("TTS_RATE", "185"))
TTS_VOLUME = float(os.getenv("TTS_VOLUME", "1.0"))
MIC_TIMEOUT = float(os.getenv("MIC_TIMEOUT", "6"))
MIC_PHRASE_LIMIT = float(os.getenv("MIC_PHRASE_LIMIT", "12"))

SYSTEM_PROMPT = f"""You are {ASSISTANT_NAME}, a concise, capable personal AI assistant running locally.
Keep spoken responses short (one to three sentences) unless the user requests detail.
Be dry-witted but genuinely helpful. Local skills handle operating-system actions before
messages reach you, so focus on conversation, explanations, and reasoning."""
