# J.A.R.V.I.S. — Double Clap Workspace Activator

Clap twice and JARVIS greets you, opens your music, and launches your full workspace automatically.

## What it does

1. Listens for **2 claps** via microphone
2. Checks internet connection:
   - **Online** — speaks *"Welcome home, sir. All systems are online and running smoothly. Opening your workspace now."*
   - **Offline** — speaks *"Welcome home, sir. Internet connection is unavailable. All systems are operating in offline mode."*
3. **Online only**: Opens YouTube + YouTube Music in the browser
4. Launches your workspace apps:
   - **Antigravity**
   - **Claude** (AI assistant)
   - **Terminal** with Claude Code CLI (`claude`) running inside

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python bienvenido_jarvis.py
```

Press `Ctrl+C` to shut down.

> **Tip:** If claps aren't detected, adjust `THRESHOLD` in the script. Increase it to reduce false triggers from background noise; decrease it if real claps aren't registering.

## Requirements

- macOS
- Python 3.9+
- Microphone
- Claude Code CLI installed (`npm install -g @anthropic-ai/claude-code` or `pip install claude-code`)
