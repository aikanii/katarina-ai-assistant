"""Katarina's listen -> skill -> brain -> speak loop."""
import sys
import config
from stt import Listener
from tts import Speaker
from skills import try_skills


def main():
    speaker, listener = Speaker(), Listener()
    brain = None
    if config.GEMINI_API_KEY:
        try:
            from brain import Brain
            brain = Brain()
        except Exception as exc:
            print(f"[main] Brain disabled: {exc}", file=sys.stderr)
    else:
        print("[main] No GEMINI_API_KEY; running with local skills only.", file=sys.stderr)

    speaker.say(f"{config.ASSISTANT_NAME} online. How can I help?")
    while True:
        try:
            text = listener.listen()
            if not text:
                continue
            response = try_skills(text)
            if response is None:
                if brain:
                    try:
                        response = brain.think(text)
                    except Exception as exc:
                        print(f"[brain] Request failed: {exc}", file=sys.stderr)
                        response = "I couldn't reach my online brain. Please try again."
                else:
                    response = "I can handle local commands, but conversation needs GEMINI_API_KEY."
            speaker.say(response)
        except (KeyboardInterrupt, EOFError):
            speaker.say("Goodbye.")
            return
        except Exception as exc:
            print(f"[main] Unexpected error: {exc}", file=sys.stderr)
            speaker.say("Sorry, something went wrong there.")


if __name__ == "__main__":
    main()
