"""Central settings for Rika. Change things here, not in the code."""

# --- Model ---
MODEL = "qwen3:4b"          # must match `ollama list`
OLLAMA_HOST = "http://localhost:11434"
THINKING = False            # Qwen3 "thinking" mode: off = fast replies (better for voice)
NO_THINK_SWITCH = True      # also send Qwen3's /no_think switch when thinking is off

# Generation options (kept modest for an RTX 3050 6 GB)
TEMPERATURE = 0.7
CONTEXT_WINDOW = 4096       # tokens; raise later if VRAM allows

# --- Conversation ---
MAX_HISTORY_MESSAGES = 20   # older turns are dropped to keep replies fast

# --- Persona ---
ASSISTANT_NAME = "Rika"
SYSTEM_PROMPT = (
    f"You are {ASSISTANT_NAME}, a friendly, concise personal AI assistant that runs "
    "fully offline on the user's own computer. Keep answers short and clear, since "
    "they may be spoken aloud. If you do not know something, say so instead of guessing."
)

# --- Voice input (speech to text) ---
START_IN_VOICE_MODE = False
SAMPLE_RATE = 16000          # Hz, what Whisper expects
INPUT_DEVICE = None          # None = default microphone; or a device number from `python -m sounddevice`

# Accuracy ladder (bigger = more accurate but slower / more memory):
#   "small"  <  "medium"  <  "large-v3-turbo" (best balance)  <  "large-v3"
WHISPER_MODEL = "large-v3-turbo"
WHISPER_DEVICE = "auto"      # "auto" tries the GPU first and falls back to CPU; or "cpu" / "cuda"
WHISPER_LANGUAGE = "en"      # None = auto-detect
WHISPER_BEAM_SIZE = 5        # higher = more accurate, a little slower
# Words Whisper often gets wrong; a short hint improves recognition of them.
WHISPER_HINT = "Conversation with Rika, a personal AI assistant. Topics: Python, Ollama, database, PDF."

# --- Voice output (text to speech, Piper) ---
SPEAK_REPLIES = True
PIPER_VOICE = "voices/en_US-amy-medium.onnx"   # run `python download_voice.py` once
