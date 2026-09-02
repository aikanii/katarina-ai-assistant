"""
Text-to-speech output. Uses pyttsx3, which works fully offline on
Windows (SAPI5), macOS (NSSpeechSynthesizer), and Linux (espeak).
"""
import sys
import config


class Speaker:
    def __init__(self):
        self.enabled = config.VOICE_ENABLED
        self.engine = None
        if self.enabled:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty("rate", config.TTS_RATE)
                self.engine.setProperty("volume", config.TTS_VOLUME)
            except Exception as e:
                print(f"[tts] Voice output unavailable ({e}); falling back to text.", file=sys.stderr)
                self.enabled = False

    def say(self, text: str):
        """Speak text aloud (if voice is enabled) and always print it."""
        print(f"Jarvis: {text}")
        if self.enabled and self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"[tts] Playback error ({e})", file=sys.stderr)
