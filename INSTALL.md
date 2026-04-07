# J.A.R.V.I.S. — Installation Manual

> **Just A Rather Very Intelligent System**
> Double-clap your way into a fully loaded workspace.

---

## Table of Contents

1. [System Requirements](#1-system-requirements)
2. [Pre-Installation: Apps to Install First](#2-pre-installation-apps-to-install-first)
3. [Clone the Repository](#3-clone-the-repository)
4. [Run the Installer](#4-run-the-installer)
5. [Grant Microphone Access](#5-grant-microphone-access)
6. [Start JARVIS](#6-start-jarvis)
7. [Test It — Do the Double Clap](#7-test-it--do-the-double-clap)
8. [What Happens on Each Double Clap](#8-what-happens-on-each-double-clap)
9. [Configuration](#9-configuration)
10. [Troubleshooting](#10-troubleshooting)
11. [Uninstall](#11-uninstall)

---

## 1. System Requirements

| Requirement | Minimum |
|-------------|---------|
| Operating System | macOS Ventura 13+ (Intel or Apple Silicon) |
| Python | 3.9 or newer |
| Microphone | Built-in or external |
| Internet | Required for initial install and online features |

---

## 2. Pre-Installation: Apps to Install First

JARVIS will try to open these apps when triggered. Install them **before** running the installer.

### Antigravity
Install Antigravity from its official source or the Mac App Store.

### Claude Desktop App
Download from [claude.ai](https://claude.ai) → click **Download for Mac** → drag to Applications.

### Claude Code CLI (`claude` command)
JARVIS opens Terminal and runs `claude` inside it. Install the CLI with one of these methods:

**Option A — via npm (recommended):**
```bash
npm install -g @anthropic-ai/claude-code
```

**Option B — via pip:**
```bash
pip install claude-code
```

Verify it works:
```bash
claude --version
```

### Python 3.9+

**Check if you already have it:**
```bash
python3 --version
```

If you see `Python 3.9.x` or higher, you're good. If not:

**Option A — Install via Homebrew (recommended):**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
```

**Option B — Download from python.org:**
Go to [python.org/downloads](https://www.python.org/downloads/) → download the latest macOS installer → run it.

---

## 3. Clone the Repository

Open **Terminal** and run:

```bash
git clone https://github.com/Srimi1/New-Jarvis.git
cd New-Jarvis
```

---

## 4. Run the Installer

This is a one-time step. The installer handles everything automatically.

```bash
chmod +x install.sh && ./install.sh
```

**What it does — and what you should see:**

```
======================================================
  J.A.R.V.I.S. — Installer
======================================================

  Python 3.x.x ......................... OK
  Virtual environment created ........... OK
  Installing dependencies (this may take a moment)...
  Dependencies installed ................ OK
  Claude Code CLI ....................... OK
  Launcher (jarvis.sh) created .......... OK

======================================================
  Installation complete!

  To run JARVIS:
    ./jarvis.sh

  IMPORTANT: When macOS asks for microphone access,
  click Allow — JARVIS needs it to hear your claps.
======================================================
```

> If you see a **WARNING** about `claude` CLI not found, install it first (see Step 2) then re-run `./install.sh`.

**What the installer creates:**

| Item | Purpose |
|------|---------|
| `.venv/` | Python virtual environment with all dependencies |
| `jarvis.sh` | Launcher script — use this to start JARVIS every time |

---

## 5. Grant Microphone Access

The **first time** you run JARVIS, macOS will show a permission dialog:

> *"Terminal" would like to access the microphone.*

Click **Allow**.

If you accidentally clicked Don't Allow:
1. Open **System Settings** → **Privacy & Security** → **Microphone**
2. Find **Terminal** in the list
3. Toggle it **ON**

Without microphone access, JARVIS cannot hear your claps.

---

## 6. Start JARVIS

Every time you want JARVIS running:

```bash
./jarvis.sh
```

You should see:

```
=======================================================
  J.A.R.V.I.S. — Online and standing by, sir.
  Awaiting double clap... (Ctrl+C to shut down)
  Sensitivity threshold: 0.2
=======================================================
```

JARVIS is now listening. Leave this Terminal window open in the background.

To shut down: press **Ctrl+C**

```
[ JARVIS ]  Powering down. Have a good evening, sir.
```

---

## 7. Test It — Do the Double Clap

With JARVIS running, clap your hands **twice** within **2 seconds**.

**Tips for reliable detection:**
- Clap firmly — a light tap may not register
- Clap within ~1 metre of your microphone
- Two distinct claps, not one continuous sound
- Watch the terminal for feedback:

```
  [ JARVIS ]  Signal detected 1/2  (RMS=0.312)
  [ JARVIS ]  Signal detected 2/2  (RMS=0.298)

[ JARVIS ]  Initializing welcome sequence...
```

If no output appears, your claps are below the threshold — see [Troubleshooting](#10-troubleshooting).

---

## 8. What Happens on Each Double Clap

```
Double clap detected
        │
        ▼
Check internet connection
        │
        ├── ONLINE ──▶ Speaks:
        │              "Welcome home, sir. All systems are online
        │               and running smoothly. Opening your workspace now."
        │              Opens YouTube video in browser
        │              Opens YouTube Music (music.youtube.com) in browser
        │
        └── OFFLINE ─▶ Speaks:
                       "Welcome home, sir. Internet connection is
                        unavailable. All systems are operating in
                        offline mode."
                       (skips browser — no YouTube)

        │ (always, regardless of internet)
        ▼
Opens Antigravity
Opens Claude desktop app
Opens Terminal → runs 'claude' (Claude Code CLI) inside it

        │
        ▼
JARVIS goes back to listening (ready for next double clap)
```

**Voice:** JARVIS uses the macOS British English voice **Daniel** (or Oliver/Alex as fallback). If none of those are installed, it falls back to your system's default voice via pyttsx3.

---

## 9. Configuration

Open `bienvenido_jarvis.py` in any text editor to customize these settings near the top of the file:

```python
# ── Audio Detection ──────────────────────────────────────
THRESHOLD     = 0.20   # Clap sensitivity (RMS level)
                       # ↑ raise to ignore background noise
                       # ↓ lower if claps aren't registering
COOLDOWN      = 0.1    # Minimum seconds between two claps
DOUBLE_WINDOW = 2.0    # Seconds you have to clap twice

# ── Media URLs ───────────────────────────────────────────
YOUTUBE_URL       = "https://www.youtube.com/watch?v=hEIexwwiKKU"
YOUTUBE_MUSIC_URL = "https://music.youtube.com/"
```

**Common adjustments:**

| Situation | Fix |
|-----------|-----|
| JARVIS triggers by accident (loud room) | Raise `THRESHOLD` to `0.30` or `0.40` |
| Claps not detected | Lower `THRESHOLD` to `0.10` or `0.15` |
| Need more time between claps | Raise `DOUBLE_WINDOW` to `3.0` |
| Want different music | Change `YOUTUBE_URL` to any YouTube link |

---

## 10. Troubleshooting

### Claps not detected — no output in terminal

**Cause:** `THRESHOLD` is set too high for your microphone/room.

**Fix:** Open `bienvenido_jarvis.py` and lower `THRESHOLD`:
```python
THRESHOLD = 0.10  # was 0.20
```

---

### Too many false triggers (JARVIS fires randomly)

**Cause:** Background noise (keyboard, music, voices) is above the threshold.

**Fix:** Raise `THRESHOLD`:
```python
THRESHOLD = 0.35
```

---

### macOS blocks microphone / no sound input

**Fix:**
1. **System Settings** → **Privacy & Security** → **Microphone**
2. Enable the toggle next to **Terminal**
3. Restart `./jarvis.sh`

---

### `claude` command not found / fails in Terminal

**Fix:** Install Claude Code CLI:
```bash
npm install -g @anthropic-ai/claude-code
```
Then re-run `./install.sh` to confirm it's detected.

---

### Antigravity or Claude app doesn't open

**Cause:** The app isn't installed, or its name in macOS doesn't match exactly.

**Fix:** Check the app name in Finder → Applications. If it's different, update the name in `bienvenido_jarvis.py`:
```python
("Antigravity", ["open", "-a", "Antigravity"]),  # ← change "Antigravity" to exact app name
```

---

### `install.sh: Permission denied`

```bash
chmod +x install.sh
./install.sh
```

---

### `python3 not found`

Install Python via Homebrew:
```bash
brew install python
```
Or download from [python.org](https://www.python.org/downloads/).

---

### `ERROR: Python 3.9+ required`

Your system Python is too old. Install a newer version:
```bash
brew install python@3.12
```
Then re-run `./install.sh`.

---

### Voice not working / silent

**Cause:** `pyttsx3` dependency issue or no system voice available.

**Fix:**
```bash
.venv/bin/pip install pyobjc
```
Then restart JARVIS.

---

### `./jarvis.sh: No such file or directory`

The installer hasn't been run yet, or it failed midway.

**Fix:** Re-run the installer:
```bash
chmod +x install.sh && ./install.sh
```

---

## 11. Uninstall

To remove everything the installer created:

```bash
rm -rf .venv jarvis.sh
```

This removes the virtual environment and launcher but keeps your source code intact. To fully remove JARVIS, delete the entire `New-Jarvis/` folder.

---

*J.A.R.V.I.S. — Stark Industries. All systems nominal.*
