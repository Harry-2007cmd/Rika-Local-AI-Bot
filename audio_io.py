"""Microphone recording and speech-to-text."""
import numpy as np
import sounddevice as sd

import config


class Listener:
    def __init__(self):
        # Imported here so text-only mode starts instantly.
        from faster_whisper import WhisperModel

        print(f"Loading speech model '{config.WHISPER_MODEL}'...")
        self.model = WhisperModel(
            config.WHISPER_MODEL,
            device=config.WHISPER_DEVICE,
            compute_type=config.WHISPER_COMPUTE,
        )

    def record(self):
        """Record until the user presses Enter. Returns float32 mono audio."""
        chunks = []

        def callback(indata, frames, time, status):
            chunks.append(indata.copy())

        with sd.InputStream(
            samplerate=config.SAMPLE_RATE, channels=1, dtype="float32", callback=callback
        ):
            input("  [recording... press Enter to stop] ")
        if not chunks:
            return np.zeros(0, dtype="float32")
        return np.concatenate(chunks).flatten()

    def transcribe(self, audio):
        if len(audio) < config.SAMPLE_RATE * 0.3:  # under 0.3 s: nothing said
            return ""
        segments, _ = self.model.transcribe(
            audio,
            language=config.WHISPER_LANGUAGE,
            vad_filter=True,
            beam_size=1,
        )
        return " ".join(s.text.strip() for s in segments).strip()

    def listen(self):
        input("  [press Enter to start speaking] ")
        return self.transcribe(self.record())
