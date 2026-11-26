"""Talks to the model. Yields text as it streams in."""
import ollama

import config


def build_messages(history):
    recent = history[-config.MAX_HISTORY_MESSAGES:]
    return [{"role": "system", "content": config.SYSTEM_PROMPT}] + recent


def stream_chunks(client, history, thinking):
    stream = client.chat(
        model=config.MODEL,
        messages=build_messages(history),
        stream=True,
        think=thinking,
        options={"temperature": config.TEMPERATURE, "num_ctx": config.CONTEXT_WINDOW},
    )
    for chunk in stream:
        text = chunk["message"]["content"]
        if text:
            yield text


def make_client():
    return ollama.Client(host=config.OLLAMA_HOST)
