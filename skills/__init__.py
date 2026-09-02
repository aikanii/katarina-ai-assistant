"""
Skill registry. Each skill is a (matcher, handler) pair:
  - matcher(text) -> True if this skill should handle the command
  - handler(text)  -> returns a string response to speak

Skills run BEFORE the LLM brain, so simple/local commands are instant,
free, and work even offline. If no skill matches, main.py falls back
to brain.think().

To add a new skill: write a function below (or in a new file in this
folder) and register it in SKILLS at the bottom.
"""
from . import system, web, apps

SKILLS = [
    *system.SKILLS,
    *web.SKILLS,
    *apps.SKILLS,
]


def try_skills(text: str):
    """Return a response string if a skill handled the command, else None."""
    lowered = text.lower().strip()
    if not lowered:
        return None
    for matcher, handler in SKILLS:
        if matcher(lowered):
            return handler(lowered)
    return None
