"""
JARVIS — personal assistant main loop.

Flow each turn:
  1. Listen (mic or typed input)
  2. Try local skills first (instant, free, works offline)
  3. If no skill matches, fall back to the Claude-powered brain
  4. Speak the response

Run:
    python main.py
"""
import sys
import config
from stt import Listener
from tts import Speaker
from skills import try_skills


def main():
    speaker = Speaker()
    listener = Listener()

    # Brain is optional — JARVIS still runs (skills-only) without an API key
    brain = None
    try:
        from brain import Brain
        brain = Brain()
    except Exception as e:
        print(f"[main] Brain disabled: {e}")
        print("[main] Set ANTHROPIC_API_KEY to enable full conversation. Skills still work.")

    speaker.say(f"{config.ASSISTANT_NAME} online. How can I help?")

    while True:
        try:
            text = listener.listen()
            if not text:
                continue

            response = try_skills(text)  # skills run first
            if response is None:
                if brain:
                    response = brain.think(text)
                else:
                    response = "I don't have a skill for that, and my brain isn't connected — set ANTHROPIC_API_KEY to enable full conversation."

            speaker.say(response)

        except KeyboardInterrupt:
            speaker.say("Goodbye.")
            sys.exit(0)
        except Exception as e:
            print(f"[main] Unexpected error: {e}", file=sys.stderr)
            speaker.say("Sorry, something went wrong there.")


if __name__ == "__main__":
    main()
