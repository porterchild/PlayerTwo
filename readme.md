# PlayerTwo

🧠 Your always-on, local AI sidekick.
PlayerTwo watches your screen, remembers everything, and helps you out — all without sending data to the cloud.

## What is PlayerTwo?

**PlayerTwo** is a privacy-first, local AI agent that runs 24/7 on your machine. It sees what you see, logs your digital context, and offers help based on full awareness of your workflow.

Some similar tools like Microsoft Recall are very sophisticated about logging and indexing, this is less about that, and more about exploring how coherently a local LLM can record, understand, store, and compress the meaning of what you do, and then help you out with things, which should be easier since it has so much context already. 

I.e. in the beginning at least, the only storage that happens is what the LLM decides to store in its own text memory. It's up to the LLM to maintain coherence over time there. Everything it captures in realtime, like screenshots, is ephemeral. 
To enable this, there will probably be two llms, one is a vision model that can interpret the screen, one is a reasoner that excels at sensemaking, and runs in the background taking a stream of content and fitting it into a narrative that enables semantic compression of the memory.

### Current Implementation is from this prompt:
based on the readme, we're going to make a quick mvp. 
I want it to use an ollama vision model (eg gemma3:4b-it-qat) to take screenshots every 5 seconds, and log what it sees to the terminal. 
Every 30 seconds, another ollama llm, this one is a pure-text reasoner (eg qwen3:4b), takes the raw log and makes a summary, and adds it to a "conceptual log". The conceptual log has the benefit of deduplication of redundant raw log entries, and the layering on of a narrative that unifies the progression of the raw log. The reasoner is trying to craft a story from the raw log. In fact, let's call the conceptual log the 'story' instead.
Details: The vision model takes in not only the screenshot, but also the recent 'story', as well as recent raw log as context. Also, the reasoner takes in the recent 'story' as well as recent raw log.

 PlayerTwo MVP

"""
PlayerTwo – Minimum‑Viable Prototype
===================================

This MVP demonstrates a local AI side‑kick that:
1. Captures a screenshot every 5 s, sending it to a vision‑capable Ollama model.
2. Logs the model's description to a *raw log* and prints it to the terminal.
3. Every 30 s, feeds the recent raw log + the running *story* to a reasoning LLM which appends a narrative summary.

* Vision model   : `gemma3:4b-it-qat` (or any Ollama vision model)
* Reasoner model : `qwen3:4b`        (or any Ollama text model)

All state lives in memory; persistence can be added later.

Run
---
```bash
pip install -r requirements.txt
python main.py
```

Configuration is in **config.py**.
"""


### Key Features

* 🖥️ **Full-Screen Context Awareness**
  Reads screen contents (optionally with OCR or OS APIs) to stay in sync with what you're doing.

* 🧠 **Persistent Memory**
  Remembers what you’ve done, seen, and written — across tabs, windows, and sessions.

* 💬 **Smart Assistant Capabilities**
  Brainstorms, summarizes, codes, writes, and automates — with contextual awareness.

* 🔒 **100% Local**
  No cloud calls, no phoning home. Your data never leaves your machine.

* ⚡ **Extensible**
  Easily integrate with LLMs (like llama.cpp, ollama, etc.), automation APIs, custom prompt chains, and more.

## Philosophy

> If an AI assistant sees everything, it must live locally.
> PlayerTwo respects your autonomy — it's powerful *because* it's private.

## Roadmap

* Live screen parsing (OCR + DOM hooks)
* Semantic activity logging
* Timeline search interface
* Native LLM integration (Ollama, llama.cpp, etc.)
* Plugin/task architecture (write email, code, summarize, etc.)

## License

MIT — feel free to use, fork, and improve.
