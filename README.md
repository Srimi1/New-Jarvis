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
   - **Claude** (AI assistant app)
   - **Terminal** with Claude Code CLI (`claude`) running inside

## Requirements

- macOS
- Python 3.9+
- Microphone
- Claude Code CLI (optional — needed for Terminal launch): [claude.ai/code](https://claude.ai/code)

## Installation

Clone the repo, then run the installer once:

```bash
chmod +x install.sh && ./install.sh
```

The installer will:
- Verify Python 3.9+
- Create a `.venv/` virtual environment
- Install all Python dependencies
- Warn if `claude` CLI is missing
- Generate a `jarvis.sh` launcher

## Usage

```bash
./jarvis.sh
```

Press `Ctrl+C` to shut down.

> **Tip:** If claps aren't detected, adjust `THRESHOLD` in `bienvenido_jarvis.py`.
> Increase it to reduce false triggers from background noise;
> decrease it if real claps aren't registering.

## macOS Permissions

The first time you run JARVIS, macOS will ask for **microphone access** — click **Allow**.
Without it, clap detection won't work.
