"""One-time download of the Piper voice into ./voices (about 60 MB)."""
import os
import urllib.request

BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium/"
FILES = ["en_US-amy-medium.onnx", "en_US-amy-medium.onnx.json"]

os.makedirs("voices", exist_ok=True)
for name in FILES:
    dest = os.path.join("voices", name)
    if os.path.exists(dest):
        print(f"{name} already there")
        continue
    print(f"Downloading {name} ...")
    urllib.request.urlretrieve(BASE + name, dest)
print("Done.")
