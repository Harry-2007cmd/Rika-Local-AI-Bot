"""Talks to the model. Yields only the final answer as it streams in."""
import ollama

import config

OPEN_TAG, CLOSE_TAG = "<think>", "</think>"


class ThinkStripper:
    """Removes <think>...</think> blocks from a stream, even when a tag is
    split across chunks."""

    def __init__(self):
        self.buf = ""
        self.inside = False
        self.started = False  # has any visible text been emitted yet?

    def feed(self, text):
        self.buf += text
        out = []
        while True:
            if self.inside:
                i = self.buf.find(CLOSE_TAG)
                if i == -1:
                    keep = len(CLOSE_TAG) - 1
                    self.buf = self.buf[-keep:]
                    break
                self.buf = self.buf[i + len(CLOSE_TAG):]
                self.inside = False
            else:
                i = self.buf.find(OPEN_TAG)
                if i == -1:
                    # hold back a possible partial "<think" at the end
                    hold = 0
                    for k in range(min(len(OPEN_TAG) - 1, len(self.buf)), 0, -1):
                        if OPEN_TAG.startswith(self.buf[-k:]):
                            hold = k
                            break
                    out.append(self.buf[: len(self.buf) - hold])
                    self.buf = self.buf[len(self.buf) - hold:]
                    break
                out.append(self.buf[:i])
                self.buf = self.buf[i + len(OPEN_TAG):]
                self.inside = True
        return self._tidy("".join(out))

    def flush(self):
        rest = "" if self.inside else self.buf
        self.buf = ""
        return self._tidy(rest)

    def _tidy(self, text):
        # drop blank space left where the thinking block was, at the very start
        if not self.started:
            text = text.lstrip()
            if text:
                self.started = True
        return text


def build_messages(history, thinking):
    recent = [dict(m) for m in history[-config.MAX_HISTORY_MESSAGES:]]
    if not thinking and config.NO_THINK_SWITCH and recent and recent[-1]["role"] == "user":
        # Qwen3 soft switch: tells the model to skip its reasoning step (faster).
        recent[-1]["content"] += " /no_think"
    return [{"role": "system", "content": config.SYSTEM_PROMPT}] + recent


def stream_chunks(client, history, thinking):
    stream = client.chat(
        model=config.MODEL,
        messages=build_messages(history, thinking),
        stream=True,
        think=thinking,
        options={"temperature": config.TEMPERATURE, "num_ctx": config.CONTEXT_WINDOW},
    )
    stripper = ThinkStripper()
    for chunk in stream:
        text = chunk["message"]["content"]  # reasoning, if any, is in message.thinking
        if text:
            visible = stripper.feed(text)
            if visible:
                yield visible
    tail = stripper.flush()
    if tail:
        yield tail


def make_client():
    return ollama.Client(host=config.OLLAMA_HOST)
