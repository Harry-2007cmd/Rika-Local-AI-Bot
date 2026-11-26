"""Central settings for Rika. Change things here, not in the code."""

# --- Model ---
MODEL = "qwen3:4b"          # must match `ollama list`
OLLAMA_HOST = "http://localhost:11434"
THINKING = False            # Qwen3 "thinking" mode: off = fast replies (better for voice)

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
WHISPER_MODEL = "small"      # "base" is faster, "small" is more accurate
WHISPER_DEVICE = "cpu"       # "cpu" is the safe default; "cuda" needs CUDA/cuDNN libs
WHISPER_COMPUTE = "int8"     # int8 on cpu, float16 on cuda
WHISPER_LANGUAGE = "en"      # None = auto-detect

# --- Voice output (text to speech, Piper) ---
SPEAK_REPLIES = True
PIPER_VOICE = "voices/en_US-amy-medium.onnx"   # run `python download_voice.py` once
