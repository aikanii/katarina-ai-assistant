"""
The 'brain': sends conversation to Gemini for anything that isn't handled
by a local skill (see skills/). Uses Gemini's built-in chat session, which
keeps the conversation history for us automatically.
"""
import config

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None


class Brain:
    def __init__(self):
        if genai is None:
            raise RuntimeError(
                "The 'google-genai' package isn't installed. Run: pip install google-genai"
            )
        if not config.GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. See config.py for setup instructions."
            )
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)
        self._chat_config = types.GenerateContentConfig(
            system_instruction=config.SYSTEM_PROMPT,
            max_output_tokens=config.MAX_TOKENS,
        )
        self.chat = self.client.chats.create(model=config.MODEL, config=self._chat_config)

    def think(self, user_text: str) -> str:
        """Send the user's message to Gemini (chat session keeps history), return the reply."""
        response = self.chat.send_message(user_text)
        text = (response.text or "").strip()
        return text or "I didn't get a response back — try again."

    def reset(self):
        self.chat = self.client.chats.create(model=config.MODEL, config=self._chat_config)
