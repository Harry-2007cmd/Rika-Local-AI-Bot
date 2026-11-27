"""Microphone recording and speech-to-text."""
import glob
import os
import sys

import numpy as np
import sounddevice as sd

import config


def _add_nvidia_dll_dirs():
    """On Windows, make pip-installed CUDA libraries (requirements-gpu.txt) findable."""
    if sys.platform != "win32":
        return
    for base in sys.path:
        for bin_dir in glob.glob(os.path.join(base, "nvidia", "*", "bin")):
            try:
                os.add_dll_directory(bin_dir)
            except OSError:
                pass
            os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")


def _gpu_available():
    try:
        import ctranslate2

        return ctranslate2.get_cuda_device_count() > 0
    except Exception:
        return False


class Listener:
    def __init__(self):
        _add_nvidia_dll_dirs()
        from faster_whisper import WhisperModel

        self._WhisperModel = WhisperModel
        want = config.WHISPER_DEVICE
        if want == "auto":
            want = "cuda" if _gpu_available() else "cpu"

        print(f"Loading speech model '{config.WHISPER_MODEL}' on {want}...")
        if want == "cuda":
            try:
                self.model = self._load("cuda", "int8_float16")
                self._warm_up()  # missing CUDA libraries show up here, not at load time
                self.device = "cuda"
                return
            except Exception as err:
                if config.WHISPER_DEVICE == "cuda":
                    raise
                print(f"(GPU not usable for speech, falling back to CPU: {str(err)[:120]})")
        self.model = self._load("cpu", "int8")
        self.device = "cpu"

    def _load(self, device, compute):
        return self._WhisperModel(config.WHISPER_MODEL, device=device, compute_type=compute)

    def _warm_up(self):
        silence = np.zeros(config.SAMPLE_RATE, dtype="float32")
        segments, _ = self.model.transcribe(silence, language=config.WHISPER_LANGUAGE)
        list(segments)

    def record(self):
        """Record until the user presses Enter. Returns float32 mono audio."""
        chunks = []

        def callback(indata, frames, time, status):
            chunks.append(indata.copy())

        with sd.InputStream(
            samplerate=config.SAMPLE_RATE,
            channels=1,
            dtype="float32",
            device=config.INPUT_DEVICE,
            callback=callback,
        ):
            input("  [recording... press Enter to stop] ")
        if not chunks:
            return np.zeros(0, dtype="float32")
        return np.concatenate(chunks).flatten()

    @staticmethod
    def _normalize(audio):
        """Bring quiet recordings up to a healthy level (big accuracy win on laptop mics)."""
        peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
        if peak < 1e-4:
            return audio
        return (audio * (0.9 / peak)).astype("float32")

    def transcribe(self, audio):
        if len(audio) < config.SAMPLE_RATE * 0.3:  # under 0.3 s: nothing said
            return ""
        segments, _ = self.model.transcribe(
            self._normalize(audio),
            language=config.WHISPER_LANGUAGE,
            beam_size=config.WHISPER_BEAM_SIZE,
            vad_filter=True,
            condition_on_previous_text=False,
            initial_prompt=config.WHISPER_HINT or None,
        )
        return " ".join(s.text.strip() for s in segments).strip()

    def listen(self):
        input("  [press Enter to start speaking] ")
        return self.transcribe(self.record())
