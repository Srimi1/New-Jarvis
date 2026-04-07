#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System

Double-clap activation → internet check → voice greeting → opens media → launches apps.

Dependencies:
    pip install sounddevice numpy pyttsx3

Usage:
    python bienvenido_jarvis.py
"""

import os
import sys
import time
import socket
import threading
import subprocess
import webbrowser

import numpy as np
import sounddevice as sd
import pyttsx3

# ──────────────────────────────────────────────────────────────────────────────
#  Configuración
# ──────────────────────────────────────────────────────────────────────────────
SAMPLE_RATE   = 44100
BLOCK_SIZE    = int(SAMPLE_RATE * 0.05)   # 50 ms por bloque
THRESHOLD     = 0.20     # RMS mínimo para contar como aplauso  ← ajusta si falla
COOLDOWN      = 0.1      # segundos de pausa mínima entre aplausos
DOUBLE_WINDOW = 2.0      # ventana de tiempo para el segundo aplauso

YOUTUBE_URL       = "https://www.youtube.com/watch?v=hEIexwwiKKU"
YOUTUBE_MUSIC_URL = "https://music.youtube.com/"

MENSAJE         = "Welcome home, sir. All systems are online and running smoothly. Opening your workspace now."
MENSAJE_OFFLINE = "Welcome home, sir. Internet connection is unavailable. All systems are operating in offline mode."

# ──────────────────────────────────────────────────────────────────────────────
#  Estado global
# ──────────────────────────────────────────────────────────────────────────────
clap_times: list[float] = []
triggered = False
lock = threading.Lock()


# ──────────────────────────────────────────────────────────────────────────────
#  Detección de aplausos
# ──────────────────────────────────────────────────────────────────────────────
def audio_callback(indata, frames, time_info, status):
    global triggered, clap_times

    if triggered:
        return

    rms = float(np.sqrt(np.mean(indata ** 2)))
    now = time.time()

    if rms > THRESHOLD:
        with lock:
            # Ignora si estamos en el cooldown del aplauso anterior
            if clap_times and (now - clap_times[-1]) < COOLDOWN:
                return

            clap_times.append(now)
            # Limpia aplausos fuera de la ventana
            clap_times = [t for t in clap_times if now - t <= DOUBLE_WINDOW]

            count = len(clap_times)
            print(f"  [ JARVIS ]  Signal detected {count}/2  (RMS={rms:.3f})")

            if count >= 2:
                triggered = True
                clap_times = []
                threading.Thread(target=secuencia_bienvenida, daemon=True).start()


# ──────────────────────────────────────────────────────────────────────────────
#  Secuencia de bienvenida
# ──────────────────────────────────────────────────────────────────────────────
def secuencia_bienvenida():
    print("\n[ JARVIS ]  Initializing welcome sequence...\n")

    if internet_disponible():
        hablar(MENSAJE)
        abrir_musica()
    else:
        print("  [ JARVIS ]  No internet connection detected.")
        hablar(MENSAJE_OFFLINE)

    abrir_espacio_trabajo()

    print("\n[ JARVIS ]  All systems nominal. Good to have you back, sir.\n")


def hablar(texto: str):
    """TTS: tries macOS 'say' with British voice first, falls back to pyttsx3."""
    print(f"  [ JARVIS ]  Vocalizing: \"{texto}\"")

    # Prefer Daniel (British English) — closest to JARVIS's accent
    for voice in ["Daniel", "Oliver", "Alex"]:
        try:
            resultado = subprocess.run(
                ["say", "-v", voice, texto],
                capture_output=True
            )
            if resultado.returncode == 0:
                return
        except (FileNotFoundError, OSError):
            break  # 'say' command not available — fall through to pyttsx3

    # Fallback: pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    # Prefer British/English voice
    british = [v for v in voices if "en_GB" in v.id or "daniel" in v.name.lower()]
    if british:
        engine.setProperty("voice", british[0].id)
        print(f"     Voice selected: {british[0].name}")
    else:
        print("     Using default voice")

    engine.setProperty("rate", 148)
    engine.say(texto)
    engine.runAndWait()


def abrir_musica():
    print(f"  [ JARVIS ]  Launching YouTube, sir...")
    webbrowser.open(YOUTUBE_URL)
    time.sleep(0.5)

    print(f"  [ JARVIS ]  Launching YouTube Music...")
    webbrowser.open(YOUTUBE_MUSIC_URL)
    time.sleep(0.5)


def abrir_espacio_trabajo():
    apps_to_open = [
        ("Antigravity", ["open", "-a", "Antigravity"]),
        ("Claude",      ["open", "-a", "Claude"]),
    ]

    for name, cmd in apps_to_open:
        print(f"  [ JARVIS ]  Initializing {name}...")
        subprocess.Popen(cmd)
        time.sleep(0.5)

    # Open Terminal and launch Claude Code CLI inside it
    print("  [ JARVIS ]  Launching Claude Code in Terminal...")
    subprocess.Popen([
        "osascript", "-e",
        'tell application "Terminal" to do script "claude"'
    ])


# ──────────────────────────────────────────────────────────────────────────────
#  Utilidades
# ──────────────────────────────────────────────────────────────────────────────
def internet_disponible() -> bool:
    """Returns True if internet is reachable (pings Google DNS)."""
    try:
        socket.setdefaulttimeout(2)
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False


# ──────────────────────────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    global triggered

    print("=" * 55)
    print("  J.A.R.V.I.S. — Online and standing by, sir.")
    print("  Awaiting double clap... (Ctrl+C to shut down)")
    print(f"  Sensitivity threshold: {THRESHOLD}")
    print("=" * 55)

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            channels=1,
            dtype="float32",
            callback=audio_callback,
        ):
            while True:
                time.sleep(0.1)
                if triggered:
                    # Espera a que la secuencia acabe y vuelve a escuchar
                    time.sleep(8)
                    triggered = False
                    print("\n[ JARVIS ]  Standing by for next command, sir.\n")
    except KeyboardInterrupt:
        print("\n\n[ JARVIS ]  Powering down. Have a good evening, sir.")
        sys.exit(0)


if __name__ == "__main__":
    main()
