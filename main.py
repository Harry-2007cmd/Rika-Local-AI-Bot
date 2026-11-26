"""Rika - terminal chat (Milestone 1).

Commands: /clear  reset the conversation
          /think  toggle Qwen3 thinking mode
          /exit   quit
"""
import sys

import ollama

import config


def build_messages(history):
    """System prompt + the most recent turns."""
    recent = history[-config.MAX_HISTORY_MESSAGES:]
    return [{"role": "system", "content": config.SYSTEM_PROMPT}] + recent


def stream_reply(client, history, thinking):
    """Print the reply as it streams in and return the full text."""
    stream = client.chat(
        model=config.MODEL,
        messages=build_messages(history),
        stream=True,
        think=thinking,
        options={
            "temperature": config.TEMPERATURE,
            "num_ctx": config.CONTEXT_WINDOW,
        },
    )
    parts = []
    for chunk in stream:
        text = chunk["message"]["content"]
        if text:
            print(text, end="", flush=True)
            parts.append(text)
    print()
    return "".join(parts)


def main():
    client = ollama.Client(host=config.OLLAMA_HOST)
    thinking = config.THINKING
    history = []

    print(f"{config.ASSISTANT_NAME} is ready ({config.MODEL}). Type /exit to quit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            continue
        if user == "/exit":
            break
        if user == "/clear":
            history.clear()
            print("(conversation cleared)")
            continue
        if user == "/think":
            thinking = not thinking
            print(f"(thinking mode {'on' if thinking else 'off'})")
            continue

        history.append({"role": "user", "content": user})
        print(f"{config.ASSISTANT_NAME}: ", end="", flush=True)
        try:
            reply = stream_reply(client, history, thinking)
        except Exception as err:  # Ollama not running, model missing, etc.
            history.pop()
            print(f"\n[error] {err}\nIs Ollama running and is '{config.MODEL}' installed?")
            continue
        history.append({"role": "assistant", "content": reply})

    print("Bye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
