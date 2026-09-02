"""
Open local applications by name. Edit APP_MAP below to match apps you
actually have installed — the names on the right must be launchable
on your OS (see _launch for how each platform is handled).
"""
import platform
import subprocess

# command name to try per OS; add your own apps here
APP_MAP = {
    "calculator": {"Windows": "calc", "Darwin": "Calculator", "Linux": "gnome-calculator"},
    "notepad": {"Windows": "notepad", "Darwin": "TextEdit", "Linux": "gedit"},
    "terminal": {"Windows": "wt", "Darwin": "Terminal", "Linux": "gnome-terminal"},
    "browser": {"Windows": "start chrome", "Darwin": "Google Chrome", "Linux": "google-chrome"},
    "spotify": {"Windows": "spotify", "Darwin": "Spotify", "Linux": "spotify"},
    "vscode": {"Windows": "code", "Darwin": "Visual Studio Code", "Linux": "code"},
}


def _open_match(t):
    return t.startswith("open ") and any(app in t for app in APP_MAP)


def _launch(app_name: str) -> bool:
    system = platform.system()
    target = APP_MAP[app_name].get(system)
    if not target:
        return False
    try:
        if system == "Darwin":
            subprocess.Popen(["open", "-a", target])
        elif system == "Windows":
            subprocess.Popen(target, shell=True)
        else:  # Linux
            subprocess.Popen([target])
        return True
    except Exception:
        return False


def _open_handler(t):
    for app in APP_MAP:
        if app in t:
            ok = _launch(app)
            return f"Opening {app}." if ok else f"Couldn't launch {app} — check the command in skills/apps.py for your OS."
    return "I don't know that app yet — add it to APP_MAP in skills/apps.py."


SKILLS = [
    (_open_match, _open_handler),
]
