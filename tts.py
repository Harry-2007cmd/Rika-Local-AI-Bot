"""Text-to-speech with Piper. Speaks sentences in a background thread so the
next sentence can be generated while the current one is playing."""
import os
import queue
import re
import threading

import numpy as np
import sounddevice as sd

import config


def clean_for_speech(text):
    """Remove markdown symbols that sound bad when read aloud."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"[*_`#>]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


class Speaker:
    def __init__(self):
        from piper import PiperVoice

        if not os.path.exists(config.PIPER_VOICE):
            raise FileNotFoundError(
                f"Voice file not found: {config.PIPER_VOICE}. Run: python download_voice.py"
            )
        self.voice = PiperVoice.load(config.PIPER_VOICE)
        self.sample_rate = self.voice.config.sample_rate
        self._queue = queue.Queue()
        self._thread = threading.Thread(target=self._worker, daemon=True)
        self._thread.start()

    def _synth(self, text):
        # Piper's Python API differs between versions; support both.
        if hasattr(self.voice, "synthesize_stream_raw"):
            for raw in self.voice.synthesize_stream_raw(text):
                yield np.frombuffer(raw, dtype=np.int16)
        else:
            for chunk in self.voice.synthesize(text):
                yield chunk.audio_int16_array

    def _worker(self):
        while True:
            text = self._queue.get()
            try:
                if text:
                    parts = list(self._synth(text))
                    if parts:
                        sd.play(np.concatenate(parts), self.sample_rate)
                        sd.wait()
            except Exception as err:
                print(f"\n[tts error] {err}")
            finally:
                self._queue.task_done()

    def say(self, text):
        text = clean_for_speech(text)
        if text:
            self._queue.put(text)

    def wait(self):
        self._queue.join()
