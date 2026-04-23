# J.A.R.V.I.S. — Double Clap Workspace Activator

> **Just A Rather Very Intelligent System**
> Clap twice. JARVIS greets you, opens your music, and launches your full workspace — automatically.

---

## What It Does

1. Listens continuously for **2 claps** via your microphone
2. Checks your internet connection:
   - **Online** — speaks *"Welcome home, sir. All systems are online and running smoothly. Opening your workspace now."*
   - **Offline** — speaks *"Welcome home, sir. Internet connection is unavailable. All systems are operating in offline mode."*
3. **Online only:** Opens a YouTube video + YouTube Music in the browser
4. Launches your full workspace:
   - **Antigravity** — visual workspace tool
   - **Claude** — AI assistant desktop app
   - **Terminal** with **Gemini CLI** (`gemini`) running inside it

---

## Requirements

| Requirement | Detail |
|-------------|--------|
| OS | macOS Ventura 13+ (Intel or Apple Silicon) |
| Python | 3.9 or newer |
| Microphone | Built-in or external |
| Gemini CLI | [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli) |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Srimi1/New-Jarvis.git
cd New-Jarvis

# 2. Install (one-time)
chmod +x install.sh && ./install.sh

# 3. Run from anywhere
jarvis
```

The installer registers `jarvis` as a global command — start it from any Terminal window, any directory, just by typing `jarvis`.

---

## Usage

```bash
jarvis
```

You'll see:
```
=======================================================
  J.A.R.V.I.S. — Online and standing by, sir.
  Awaiting double clap... (Ctrl+C to shut down)
  Sensitivity threshold: 0.2
=======================================================
```

**Clap twice** within 2 seconds → JARVIS activates your workspace.

Press `Ctrl+C` to shut down.

---

## Configuration

Edit `bienvenido_jarvis.py` to customize:

```python
THRESHOLD     = 0.20   # Clap sensitivity — raise to reduce false triggers
COOLDOWN      = 0.1    # Min seconds between two detected claps
DOUBLE_WINDOW = 2.0    # Seconds allowed to complete the double clap

YOUTUBE_URL       = "https://www.youtube.com/watch?v=hEIexwwiKKU"
YOUTUBE_MUSIC_URL = "https://music.youtube.com/"
```

---

## macOS Permissions

The first time you run JARVIS, macOS will ask for **microphone access** — click **Allow**.
Without it, clap detection won't work.

To re-enable: **System Settings → Privacy & Security → Microphone → Terminal → ON**

---

## Full Installation Guide

See [INSTALL.md](INSTALL.md) for a step-by-step walkthrough including troubleshooting.

---

*J.A.R.V.I.S. — Stark Industries. All systems nominal.*
