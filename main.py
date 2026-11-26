"""Rika - chat in the terminal, by text or by voice.

Commands: /voice  toggle voice input (speak instead of typing)
          In voice mode say "text mode" to go back to typing, "goodbye" to quit
          /mute   toggle spoken replies
          /clear  reset the conversation
          /think  toggle Qwen3 thinking mode
          /exit   quit
"""
import os
import re
import sys

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

import brain
import config

SENTENCE_END = re.compile(r"(?<=[.!?])\s+|\n+")

# Things you can say in voice mode (matched against the whole sentence).
VOICE_OFF_PHRASES = {"text mode", "stop voice", "voice off", "exit voice mode", "stop listening"}
QUIT_PHRASES = {"exit", "quit", "goodbye", "bye", "good bye"}


def spoken_command(text):
    """Return 'text', 'quit' or None for a transcribed sentence."""
    t = re.sub(r"[^a-z ]", "", text.lower()).strip()
    if t in VOICE_OFF_PHRASES:
        return "text"
    if t in QUIT_PHRASES:
        return "quit"
    return None


def reply(client, history, thinking, speaker):
    """Stream the reply to the screen and speak it sentence by sentence."""
    full, buffer = [], ""
    for text in brain.stream_chunks(client, history, thinking):
        print(text, end="", flush=True)
        full.append(text)
        if speaker:
            buffer += text
            parts = SENTENCE_END.split(buffer)
            for sentence in parts[:-1]:
                speaker.say(sentence)
            buffer = parts[-1]
    print()
    if speaker:
        speaker.say(buffer)
        speaker.wait()
    return "".join(full)


def load_speaker():
    try:
        from tts import Speaker

        return Speaker()
    except Exception as err:
        print(f"(voice output unavailable: {err})")
        return None


def load_listener():
    try:
        from audio_io import Listener

        return Listener()
    except Exception as err:
        print(f"(voice input unavailable: {err})")
        return None


def main():
    client = brain.make_client()
    thinking = config.THINKING
    history = []
    listener = speaker = None
    voice_mode = config.START_IN_VOICE_MODE
    speak = config.SPEAK_REPLIES

    if speak or voice_mode:
        speaker = load_speaker()
    if voice_mode:
        listener = load_listener()
        voice_mode = listener is not None

    print(f"{config.ASSISTANT_NAME} is ready ({config.MODEL}). Type /exit to quit, /voice to talk.\n")
    while True:
        try:
            if voice_mode:
                print("You (voice):")
                user = listener.listen()
                print(f"You said: {user}" if user else "(didn't catch anything)")
                cmd = spoken_command(user)
                if cmd == "text":
                    voice_mode = False
                    print("(voice input off, back to typing)")
                    continue
                if cmd == "quit":
                    break
            else:
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
        if user == "/mute":
            speak = not speak
            if speak and speaker is None:
                speaker = load_speaker()
            print(f"(spoken replies {'on' if speak else 'off'})")
            continue
        if user == "/voice":
            if listener is None:
                listener = load_listener()
            voice_mode = listener is not None and not voice_mode
            print(f"(voice input {'on' if voice_mode else 'off'})")
            continue

        history.append({"role": "user", "content": user})
        print(f"{config.ASSISTANT_NAME}: ", end="", flush=True)
        try:
            text = reply(client, history, thinking, speaker if speak else None)
        except Exception as err:
            history.pop()
            print(f"\n[error] {err}\nIs Ollama running and is '{config.MODEL}' installed?")
            continue
        history.append({"role": "assistant", "content": text})

    print("Bye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
