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

[Desktop Entry]

Type=Application
Exec=/home/roshan/voicekeyboard/start_voicekeyboard.sh

Hidden=false
NoDisplay=false

X-GNOME-Autostart-enabled=true
Name=Voice Keyboard

Comment=Launch the offline voice-enabled keyboard with grammar correction
Icon=/home/roshan/voicekeyboard/icons/mic_on.png
# Vosk Models Directory

This folder is a placeholder for Vosk speech recognition models used by the voice keyboard system.

---

Do Not Upload Full Models Here

Vosk models are large (typically 100–500 MB) and should *not* be committed to this repository.  
Instead, users should download them manually and place them in this folder.


Recommended Model

We recommend the *English model* vosk-model-en-us-0.22 for best accuracy and compatibility.

Voice Keyboard Setup Instructions

Welcome to the Voice Keyboard system — a native, intelligent input tool powered by voice recognition, grammar correction, and seamless app integration.

This guide walks you through installing dependencies, downloading required models, launching the app, and enabling autostart.

Folder Structure Overview

Vosk models are large and not included in this repo.

Download the recommended English model:

vosk-model-en-us-0.22

Extract it into:

bash
voicekeyboard/models/vosk-model-en-us-0.22/

Step 3: Download LanguageTool
Download and extract:

LanguageTool 6.3

Place languagetool-server.jar in:

bash
/home/yourusername/languagetool/

Step 4: Launch the App
Run the unified launcher script:

bash
bash ~/voicekeyboard/start_voicekeyboard.sh
This will:

Start the grammar server (if available)

Launch the PyQt voice keyboard app

Step 5: Enable Autostart (Optional)
Create a .desktop file in ~/.config/autostart/:

ini
[Desktop Entry]
Type=Application
Exec=/home/yourusername/voicekeyboard/start_voicekeyboard.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=VoiceKeyboard
Comment=Launches voice keyboard and grammar server
Make it executable:

bash
chmod +x ~/.config/autostart/voicekeyboard.desktop
🧪 Step 6: Test the Flow
Click the tray icon to open the widget

Speak into the mic → text appears

Toggle grammar correction

Click "Insert" to inject text into active app

Click "Keyboard" to open onboard keyboard
