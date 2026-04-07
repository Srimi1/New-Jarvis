#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System

Double-clap activation → voice greeting → opens media (YouTube / YouTube Music) → 
simultaneously opens Antigravity, Claude, Terminal, Discord, and Cursor.

Dependencies:
    pip install sounddevice numpy pyttsx3

Usage:
    python bienvenido_jarvis.py
"""

import os
import sys
import time
import threading
import subprocess
import webbrowser

import numpy as np
import sounddevice as sd
import pyttsx3

# ──────────────────────────────────────────────────────────────────────────────
#  Configuración
# ──────────────────────────────────────────────────────────────────────────────
SAMPLE_RATE    = 44100
BLOCK_SIZE     = int(SAMPLE_RATE * 0.05)   # 50 ms por bloque
THRESHOLD      = 0.20     # RMS mínimo para contar como aplauso  ← ajusta si falla
COOLDOWN       = 0.1    # segundos de pausa mínima entre aplausos
DOUBLE_WINDOW  = 2.0     # ventana de tiempo para el segundo aplauso

# URLs de Medios (puedes agregar tu URL de YouTube Music aquí)
YOUTUBE_URL    = "https://www.youtube.com/watch?v=hEIexwwiKKU"
YOUTUBE_MUSIC_URL = ""  # Ejemplo: "https://music.youtube.com/watch?v=..."

MENSAJE        = "Welcome home, sir. All systems are online and running smoothly. Opening your workspace now."
NEW_PROJECT    = os.path.expanduser("~/Desktop/stark_industries")

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
            if clap_times and (now - clap_times[-1]) < COOLDOWN:
                return

            clap_times.append(now)
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

    hablar(MENSAJE)
    abrir_musica()
    abrir_espacio_trabajo()

    print("\n[ JARVIS ]  All systems nominal. Good to have you back, sir.\n")


def hablar(texto: str):
    """TTS local con pyttsx3 (usa voces del sistema, sin API key)."""
    print(f"  [ JARVIS ]  Vocalizing: \"{texto}\"")

    for voice in ["Daniel", "Oliver", "Alex"]:
        resultado = subprocess.run(
            ["say", "-v", voice, texto],
            capture_output=True
        )
        if resultado.returncode == 0:
            return

    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

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
    if YOUTUBE_URL:
        print(f"  [ JARVIS ]  Launching YouTube, sir...")
        webbrowser.open(YOUTUBE_URL)
        time.sleep(0.5)
        
    if YOUTUBE_MUSIC_URL:
        print(f"  [ JARVIS ]  Launching YouTube Music...")
        webbrowser.open(YOUTUBE_MUSIC_URL)
        time.sleep(0.5)


def abrir_espacio_trabajo():
    os.makedirs(NEW_PROJECT, exist_ok=True)

    apps_to_open = [
        ("Antigravity", ["open", "-a", "Antigravity"]),
        ("Claude", ["open", "-a", "Claude"]),
        ("Terminal", ["open", "-a", "Terminal"]),
        ("Discord", ["open", "-a", "Discord"])
    ]

    for name, cmd in apps_to_open:
        print(f"  [ JARVIS ]  Initializing {name}...")
        subprocess.Popen(cmd)
        time.sleep(0.5)

    print("  [ JARVIS ]  Loading Stark Industries workspace in Cursor...")
    cursor_cmd = encontrar_cursor()
    if cursor_cmd:
        subprocess.Popen([cursor_cmd, NEW_PROJECT])
    else:
        subprocess.Popen(["open", "-a", "Cursor", NEW_PROJECT])


# ──────────────────────────────────────────────────────────────────────────────
#  Utilidades
# ──────────────────────────────────────────────────────────────────────────────
def encontrar_cursor():
    """Devuelve la ruta del CLI de Cursor si está disponible."""
    candidatos = [
        "/usr/local/bin/cursor",
        "/opt/homebrew/bin/cursor",
        os.path.expanduser("~/.cursor/bin/cursor"),
    ]
    for path in candidatos:
        if os.path.isfile(path):
            return path
    result = subprocess.run(["which", "cursor"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    return None


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
                    time.sleep(8)
                    triggered = False
                    print("\n[ JARVIS ]  Standing by for next command, sir.\n")
    except KeyboardInterrupt:
        print("\n\n[ JARVIS ]  Powering down. Have a good evening, sir.")
        sys.exit(0)


if __name__ == "__main__":
    main()
