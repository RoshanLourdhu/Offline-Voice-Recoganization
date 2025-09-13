Offline Voice Keyboard with Grammar Correction
Project Overview

This project implements a system-wide, offline-capable voice keyboard designed to enhance accessibility and productivity.
It provides a floating textbox with microphone input, real-time speech-to-text transcription (using Vosk), and grammar correction (using LanguageTool).

The solution is lightweight, works without internet once models are installed, and integrates seamlessly with any active application by injecting text into the currently focused window.

Features

Voice Input — Offline speech-to-text using Vosk

Grammar Correction — Local LanguageTool
server for grammar and spelling checks

Keyboard Integration — System on-screen keyboard can be opened with one click

Text Injection — Insert transcribed and corrected text directly into any active app (browser, editor, etc.)

Floating UI

Mic button → start/stop voice recognition

Grammar correction toggle → enable/disable grammar checks

Insert button → paste final text into active app

Keyboard button → open system keyboard

Close button → hide window

Architecture

Frontend UI

Built with PyQt5

Floating widget + textbox + control buttons

Speech Recognition

Vosk Model
 (vosk-model-en-us-0.22)

Runs fully offline

Grammar Correction

Local LanguageTool HTTP server (Java)

Periodic grammar check while typing/speaking

System Integration

xdotool used to insert text into active windows

onboard provides optional on-screen keyboard

Requirements

Ubuntu 22.04+ (tested in VirtualBox)

Python 3.8+

Java (for LanguageTool)

Install dependencies:

sudo apt install python3-pyqt5 onboard xdotool
pip install vosk requests

 Setup Instructions

Install Vosk Model

Download vosk-model-en-us-0.22 from Vosk Models

Extract into:

~/vosk-models/vosk-model-en-us-0.22/


Install LanguageTool

Download LanguageTool 6.4

Extract into:

~/languagetool/


Start server:

java -cp languagetool-server.jar org.languagetool.server.HTTPServer --port 8081


Run Application

python3 voice_keyboard_app.py

Startup script for Voice Keyboard

1. Start Grammar Server (LanguageTool)
   
echo "Starting LanguageTool grammar server..."
nohup java -cp /home/roshan/languagetool/languagetool-server.jar \
    org.languagetool.server.HTTPServer --port 8081 > /tmp/languagetool.log 2>&1 &

2. Wait for server to come up ---
sleep 5

3. Start Voice Keyboard App ---
echo "Starting Voice Keyboard App..."
python3 /home/roshan/voicekeyboard/voice_keyboard_app.py > /tmp/voicekeyboard.log 2>&1 &
