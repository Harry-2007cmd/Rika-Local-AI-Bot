# Rika dev log

Demo to teacher: **14 Dec 2026**. Branch: `version-1`. Local folder: `D:\Rika Bot`.

## 25 Nov 2026
- Restarted the project from scratch with a fresh plan and a roadmap built backwards from the demo date.
- Stack chosen: Ollama + `qwen3:4b` (brain), faster-whisper (speech in), Piper (speech out), PyMuPDF + small embeddings + ChromaDB/FAISS (documents, planned), DuckDuckGo search (web, planned).
- Installed Ollama and tested `qwen3:4b` in the terminal.
- Created the GitHub repo and the `version-1` branch.

## 26 Nov 2026
- **Milestone 1 done:** terminal chat loop with streaming replies, history (last 20 messages), thinking mode off by default. Commands: `/clear`, `/think`, `/exit`. Tested by the user, works.
- **Milestone 2 built (voice loop):** press Enter to start and stop recording, faster-whisper `small` (CPU, int8) transcribes, Piper (Amy voice) speaks replies sentence by sentence. Commands: `/voice`, `/mute`.
- Spoken commands in voice mode: "text mode" / "stop voice" / "voice off" to return to typing, "goodbye" / "exit" / "quit" to quit.
- Silenced the Hugging Face symlink warning.
- First voice run crashed once during the initial model download; it did not happen again on the second run.
- Confirmed all components are free and open source and run offline after the one-time downloads.

## Status
| Milestone | Status |
|---|---|
| 1. Text chat | Done and tested |
| 2. Voice loop | Pushed; loads and runs, real voice exchange still to be tested |
| 3. Document / PDF search | Not started (planned 2-5 Dec) |
| 4. Tool calling / web search | Not started (6-8 Dec) |
| 5. Permissions and memory | Not started (9-10 Dec) |
| Polish, rehearsal | 11-13 Dec |

## Next time
1. Test a full voice exchange (speak, hear Rika answer); note recognition accuracy and time to first spoken word.
2. If slow, try `WHISPER_MODEL = "base"` in `config.py`.
3. Check the microphone device is the right one; add a device setting if not.
4. Then start milestone 3: PDF/text/DOCX search limited to allowed folders, with the source file named in answers.

## Notes
- Rika can read no files yet. Planned types: PDF, TXT, Markdown, DOCX. Scanned PDFs and images (OCR) are out of scope for now.
- The shell hook that warns about "unpushed commits" is a false alarm in the cloud session (shallow clone has no tracking ref); the remote branch was verified to match each time.
