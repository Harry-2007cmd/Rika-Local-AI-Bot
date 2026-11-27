# Rika-Local-AI-Bot

A fully local personal AI assistant (text and voice now, document search next). Runs on your own PC through Ollama, nothing leaves the machine.

## Setup (Windows)

```powershell
cd "D:\Rika Bot"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python download_voice.py      # one time, downloads the Piper voice (~60 MB)
```

Make sure Ollama is running and the model is installed (`ollama list` should show `qwen3:4b`).

## Run

```powershell
python main.py
```

Commands inside the chat:


| Command | What it does |
|---|---|
| `/voice` | Toggle voice input: press Enter, speak, press Enter again. In voice mode say "text mode" to go back to typing, "goodbye" to quit |
| `/mute` | Toggle spoken replies |
| `/clear` | Reset the conversation |
| `/think` | Toggle Qwen3 thinking mode |
| `/exit` | Quit |

Settings (model, persona, Whisper size, voice file) live in `config.py`.

### Better speech recognition
The default is `large-v3-turbo` (about 1.6 GB, downloaded on first `/voice`). It uses your NVIDIA GPU if it can, otherwise the CPU. For GPU speed run `pip install -r requirements-gpu.txt`. If it is too slow or uses too much memory, set `WHISPER_MODEL = "small"` or `"medium"` in `config.py`.

## Roadmap

1. Text chat loop (done)
2. Voice loop: faster-whisper in, Piper out (this milestone)
3. Document / PDF search
4. Tool calling (web search)
5. Permissions and memory
