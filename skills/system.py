"""System-level skills: time, date, volume, shutdown/sleep, exit."""
import datetime
import platform
import subprocess
import sys


def _matches(text: str, *phrases) -> bool:
    return any(p in text for p in phrases)


# --- time / date ---
def _time_match(t):
    return _matches(t, "what time", "current time", "tell me the time")


def _time_handler(t):
    now = datetime.datetime.now().strftime("%I:%M %p").lstrip("0")
    return f"It's {now}."


def _date_match(t):
    return _matches(t, "what date", "today's date", "what day is it")


def _date_handler(t):
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    return f"Today is {today}."


# --- volume (cross-platform best-effort) ---
def _volume_match(t):
    return _matches(t, "volume up", "volume down", "mute", "unmute")


def _volume_handler(t):
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            if "mute" in t and "unmute" not in t:
                subprocess.run(["osascript", "-e", "set volume output muted true"])
            elif "unmute" in t:
                subprocess.run(["osascript", "-e", "set volume output muted false"])
            elif "up" in t:
                subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 10)"])
            elif "down" in t:
                subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"])
            return "Done."
        elif system == "Windows":
            # Requires no extra deps for a rough toggle; fine-grained control
            # needs the 'pycaw' package — see README for the optional upgrade.
            return "Volume control on Windows needs the optional 'pycaw' package — see README."
        else:  # Linux
            if "mute" in t and "unmute" not in t:
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "mute"])
            elif "unmute" in t:
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "unmute"])
            elif "up" in t:
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
            elif "down" in t:
                subprocess.run(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
            return "Done."
    except Exception as e:
        return f"Couldn't change the volume ({e})."


# --- help / capabilities ---
def _help_match(t):
    return t in {"help", "what can you do", "capabilities", "commands"}


def _help_handler(t):
    return "I can tell the time or date, search the web, open common apps and sites, control volume, and chat when Gemini is configured."


# --- exit ---
def _exit_match(t):
    return _matches(t, "goodbye", "exit", "quit", "shut down jarvis", "stop listening")


def _exit_handler(t):
    print("[system] Shutting down JARVIS.")
    sys.exit(0)


SKILLS = [
    (_time_match, _time_handler),
    (_date_match, _date_handler),
    (_volume_match, _volume_handler),
    (_help_match, _help_handler),
    (_exit_match, _exit_handler),
]
