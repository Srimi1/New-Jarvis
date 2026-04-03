#!/usr/bin/env python3
"""
J.A.R.V.I.S. - Just A Rather Very Intelligent System

Double-clap activation → voice greeting → opens music → Claude + Cursor side by side.

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

YOUTUBE_URL    = "https://www.youtube.com/watch?v=hEIexwwiKKU"
MENSAJE        = "Welcome home, sir. All systems are online and ready."
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

    hablar(MENSAJE)
    abrir_youtube()
    abrir_apps_lado_a_lado()

    print("\n[ JARVIS ]  All systems nominal. Good to have you back, sir.\n")


def hablar(texto: str):
    """TTS local con pyttsx3 (usa voces del sistema, sin API key)."""
    print(f"  [ JARVIS ]  Vocalizing: \"{texto}\"")

    # Prefer Daniel (British English) — closest to JARVIS's accent
    for voice in ["Daniel", "Oliver", "Alex"]:
        resultado = subprocess.run(
            ["say", "-v", voice, texto],
            capture_output=True
        )
        if resultado.returncode == 0:
            return

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


def abrir_youtube():
    print(f"  [ JARVIS ]  Launching music, sir...")
    webbrowser.open(YOUTUBE_URL)
    time.sleep(1.2)


def abrir_apps_lado_a_lado():
    sw, sh = obtener_resolucion_pantalla()
    mitad = sw // 2

    # Asegura que existe la carpeta del nuevo proyecto
    os.makedirs(NEW_PROJECT, exist_ok=True)

    # ── Open Claude ──────────────────────────────────────────────────────────
    print("  [ JARVIS ]  Bringing up AI interface...")
    subprocess.Popen(["open", "-a", "Claude"])
    time.sleep(1.8)

    # ── Open Cursor with project ─────────────────────────────────────────────
    print("  [ JARVIS ]  Loading Stark Industries workspace...")
    cursor_cmd = encontrar_cursor()
    if cursor_cmd:
        subprocess.Popen([cursor_cmd, NEW_PROJECT])
    else:
        subprocess.Popen(["open", "-a", "Cursor", NEW_PROJECT])
    time.sleep(1.8)

    # ── Arrange windows side by side via AppleScript ─────────────────────────
    print("  [ JARVIS ]  Configuring holographic display...")
    applescript = f"""
    tell application "System Events"
        try
            tell process "Claude"
                set frontmost to true
                set position of window 1 to {{0, 0}}
                set size of window 1 to {{{mitad}, {sh}}}
            end tell
        end try
        try
            tell process "Cursor"
                set frontmost to true
                set position of window 1 to {{{mitad}, 0}}
                set size of window 1 to {{{mitad}, {sh}}}
            end tell
        end try
    end tell
    """
    subprocess.run(["osascript", "-e", applescript], capture_output=True)


# ──────────────────────────────────────────────────────────────────────────────
#  Utilidades
# ──────────────────────────────────────────────────────────────────────────────
def obtener_resolucion_pantalla() -> tuple[int, int]:
    try:
        out = subprocess.run(
            ["osascript", "-e",
             "tell application \"Finder\" to get bounds of window of desktop"],
            capture_output=True, text=True
        ).stdout.strip()
        parts = [int(x.strip()) for x in out.split(",")]
        return parts[2], parts[3]
    except Exception:
        return 1920, 1080


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
    # Intenta por PATH
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
                    # Espera a que la secuencia acabe y vuelve a escuchar
                    time.sleep(8)
                    triggered = False
                    print("\n[ JARVIS ]  Standing by for next command, sir.\n")
    except KeyboardInterrupt:
        print("\n\n[ JARVIS ]  Powering down. Have a good evening, sir.")
        sys.exit(0)


if __name__ == "__main__":
    main()
