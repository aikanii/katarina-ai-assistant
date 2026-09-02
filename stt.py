"""
Speech-to-text input. Uses the `speech_recognition` library with Google's
free web recognizer by default (needs internet, no API key required).

Uses PyAudio when available and sounddevice on Python versions without a
compatible PyAudio wheel. Falls back to keyboard input if no microphone is
available.
"""
import sys
import time

import config


class Listener:
    def __init__(self):
        self.enabled = config.VOICE_ENABLED
        self.recognizer = None
        self.mic = None
        self.sounddevice = None
        self.numpy = None
        if self.enabled:
            try:
                import speech_recognition as sr
                self.sr = sr
                self.recognizer = sr.Recognizer()
            except Exception as e:
                print(f"[stt] Speech recognition unavailable ({e}); falling back to typed input.", file=sys.stderr)
                self.enabled = False
                return

            try:
                self.mic = sr.Microphone()
                with self.mic as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                self.backend = "pyaudio"
            except Exception:
                try:
                    import numpy as np
                    import sounddevice as sd
                    sd.query_devices(kind="input")
                    self.numpy = np
                    self.sounddevice = sd
                    self.backend = "sounddevice"
                    print("[stt] Using sounddevice microphone backend.")
                except Exception as e:
                    print(f"[stt] Microphone unavailable ({e}); falling back to typed input.", file=sys.stderr)
                    self.enabled = False

    def listen(self) -> str:
        """Return the user's next command as text, via mic or keyboard."""
        if not self.enabled:
            return input("You: ").strip()

        print("Listening...")
        try:
            if self.backend == "sounddevice":
                audio = self._listen_sounddevice()
            else:
                with self.mic as source:
                    audio = self.recognizer.listen(
                        source,
                        timeout=config.MIC_TIMEOUT,
                        phrase_time_limit=config.MIC_PHRASE_LIMIT,
                    )
            if audio is None:
                return ""
            text = self.recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text
        except self.sr.WaitTimeoutError:
            return ""
        except self.sr.UnknownValueError:
            print("[stt] Didn't catch that.")
            return ""
        except Exception as e:
            print(f"[stt] Recognition error ({e}); falling back to typed input this turn.", file=sys.stderr)
            return input("You: ").strip()

    def _listen_sounddevice(self):
        """Capture one phrase and return it in SpeechRecognition's format."""
        sample_rate = 16000
        chunk_size = 1024
        silence_limit = 0.8
        started_at = None
        last_voice_at = None
        chunks = []

        with self.sounddevice.InputStream(
            samplerate=sample_rate,
            channels=1,
            dtype="int16",
            blocksize=chunk_size,
        ) as stream:
            deadline = time.monotonic() + config.MIC_TIMEOUT
            while True:
                chunk, _ = stream.read(chunk_size)
                chunk = chunk.copy()
                level = float(self.numpy.abs(chunk.astype(self.numpy.int32)).mean())
                now = time.monotonic()

                if started_at is None:
                    if level < self.recognizer.energy_threshold:
                        if now >= deadline:
                            return None
                        continue
                    started_at = now

                chunks.append(chunk)
                if level >= self.recognizer.energy_threshold:
                    last_voice_at = now
                elif last_voice_at and now - last_voice_at >= silence_limit:
                    break
                elif now - started_at >= config.MIC_PHRASE_LIMIT:
                    break

        audio_bytes = self.numpy.concatenate(chunks).tobytes()
        return self.sr.AudioData(audio_bytes, sample_rate, 2)
