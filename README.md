# Katarina — your own AI assistant

A voice-enabled personal assistant with a "skills" system for instant local
actions (open apps, search the web, check the time, control volume) and a
Gemini-powered "brain" for everything else (real conversation, questions,
reasoning).

## How it works

Every time you speak or type a command:
1. **Skills check first** — fast, free, offline pattern-matched actions
   (`skills/system.py`, `skills/web.py`, `skills/apps.py`).
2. **If no skill matches**, the command goes to Gemini (`brain.py`) for a
   real conversational response.
3. The response is spoken aloud via text-to-speech.

This split is why Katarina feels instant for commands like "what time is it"
but can still hold a real conversation for anything open-ended.

## 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Note on PyAudio** (needed for microphone input):
- **Windows**: usually installs fine via pip.
- **Python 3.14 on Windows**: uses `sounddevice` instead, since PyAudio does not yet provide a compatible wheel.
- **macOS**: `brew install portaudio` first, then `pip install pyaudio`.
- **Linux**: `sudo apt install portaudio19-dev python3-pyaudio` first.

If PyAudio fails to install, don't worry — JARVIS automatically falls back
to typed input, everything else still works.

## 2. Set your API key

Get a free key from https://aistudio.google.com/apikey, then:

```bash
cp .env.example .env
```

Open `.env` and paste your key in:
```
GEMINI_API_KEY=AIza...
```

That's it — `config.py` loads `.env` automatically. Your key stays local:
`.env` is already listed in `.gitignore`, so `git` will never pick it up,
even if you push this project to GitHub.

Without a key, Katarina still runs and handles all local skills — it just
can't have open-ended conversations.

## 3. Run it

```bash
python main.py
```

Try saying (or typing):
- "What time is it?"
- "Search for best pizza near me"
- "Open notepad" / "open browser" / "open spotify"
- "Volume up" / "mute"
- Anything else — it'll go straight to Gemini, e.g. "explain quantum entanglement simply"
- "Goodbye" to exit

## Extending it

### Add a new skill
Create or edit a file in `skills/`, define a `(matcher, handler)` pair, and
add it to that file's `SKILLS` list:

```python
def _matches(t):
    return "tell me a joke" in t

def _handler(t):
    return "Why did the developer go broke? They used up all their cache."

SKILLS = [(_matches, _handler)]
```

Then import and include it in `skills/__init__.py`.

### Add more apps
Edit `APP_MAP` in `skills/apps.py` — add the app name and the correct
launch command per OS.

### Smart home control
Not included by default since it depends heavily on your specific
ecosystem (Home Assistant, Google Home, Philips Hue, etc.). The cleanest
path: stand up [Home Assistant](https://www.home-assistant.io/) with its
REST API enabled, then add a new `skills/smart_home.py` that sends HTTP
requests to it — same `(matcher, handler)` pattern as the other skills.

### Wake word / always-listening
Right now JARVIS listens for one phrase, processes it, then listens again
(push-to-talk style via Enter, or continuous with pauses). For a true
"Hey Jarvis" wake word without an always-on cloud connection, look at the
`openwakeword` or `porcupine` (Picovoice) libraries — swap `stt.py`'s
`listen()` to wait for the wake word before capturing the full command.

### Swap the speech engine
- Faster/offline recognition: swap Google's recognizer in `stt.py` for
  [OpenAI Whisper](https://github.com/openai/whisper) (`pip install
  openai-whisper`) run locally.
- More natural voice: swap `pyttsx3` in `tts.py` for a cloud TTS API
  (ElevenLabs, Azure, etc.) if you don't mind the API cost/latency.

## Project structure

```
jarvis/
├── main.py           # the loop: listen → skill or brain → speak
├── config.py          # settings, API key, personality/system prompt
├── stt.py              # speech-to-text (mic, falls back to typing)
├── tts.py              # text-to-speech (offline)
├── brain.py            # Gemini API conversation
├── requirements.txt
├── .env.example        # template — copy to .env and add your key
├── .gitignore           # keeps .env (and venv, caches) out of git
└── skills/
    ├── __init__.py     # skill registry / router
    ├── system.py        # time, date, volume, exit
    ├── web.py            # search, open websites
    └── apps.py            # launch local applications
```
