# Rika-Local-AI-Bot

A fully local personal AI assistant (text now, voice and document search next). Runs on your own PC through Ollama, nothing leaves the machine.

## Setup (Windows)

```powershell
cd "D:\Rika Bot"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Make sure Ollama is running and the model is installed (`ollama list` should show `qwen3:4b`).

## Run

```powershell
python main.py
```

Commands inside the chat: `/clear` resets the conversation, `/think` toggles Qwen3 thinking mode, `/exit` quits.

Settings (model, persona, history length) live in `config.py`.

## Roadmap

1. Text chat loop (this milestone)
2. Voice loop (faster-whisper + Piper)
3. Document / PDF search
4. Tool calling (web search)
5. Permissions and memory
