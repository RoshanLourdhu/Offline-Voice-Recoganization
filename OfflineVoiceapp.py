import sys
import subprocess
import json
import requests
import threading
import pyaudio
from vosk import Model, KaldiRecognizer

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QCheckBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer, QMetaObject, Q_ARG

# ------------------ CONFIG ------------------ #
MODEL_PATH = "/home/roshan/vosk-models/vosk-model-en-us-0.22"
LANGUAGETOOL_URL = "http://localhost:8081/v2/check"

# Load Vosk model
model = Model(MODEL_PATH)


class VoiceKeyboardApp(QWidget):
    def _init_(self):
        super()._init_()

        # ---- UI Setup ----
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry(200, 200, 500, 250)
        self.setWindowTitle("Voice Keyboard")

        layout = QVBoxLayout()

        # Text area
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("Speak or type here...")
        layout.addWidget(self.text_box)

        # Grammar correction checkbox
        self.grammar_checkbox = QCheckBox("Enable Grammar Correction")
        self.grammar_checkbox.setChecked(True)
        layout.addWidget(self.grammar_checkbox)

        # Buttons row
        btn_layout = QHBoxLayout()

        self.mic_button = QPushButton("🎤 Mic")
        self.mic_button.clicked.connect(self.toggle_mic)
        btn_layout.addWidget(self.mic_button)

        self.keyboard_button = QPushButton("⌨ Keyboard")
        self.keyboard_button.clicked.connect(self.open_keyboard)
        btn_layout.addWidget(self.keyboard_button)

        self.insert_button = QPushButton("➡ Insert")
        self.insert_button.clicked.connect(self.insert_text)
        btn_layout.addWidget(self.insert_button)

        self.close_button = QPushButton("❌ Close")
        self.close_button.clicked.connect(self.close)
        btn_layout.addWidget(self.close_button)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        # ---- Speech recognition ----
        self.mic_active = False
        self.thread = None

        # ---- Grammar correction timer ----
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_grammar)
        self.timer.start(2000)

    # ------------------ Mic Handling ------------------ #
    def toggle_mic(self):
        if not self.mic_active:
            self.mic_active = True
            self.mic_button.setText("🛑 Stop")
            self.thread = threading.Thread(target=self.run_vosk, daemon=True)
            self.thread.start()
        else:
            self.mic_active = False
            self.mic_button.setText("🎤 Mic")

    def run_vosk(self):
        rec = KaldiRecognizer(model, 16000)
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=2048,
        )
        stream.start_stream()

        while self.mic_active:
            data = stream.read(2048, exception_on_overflow=False)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    QMetaObject.invokeMethod(
                        self.text_box,
                        "insertPlainText",
                        Qt.QueuedConnection,
                        Q_ARG(str, text + " "),
                    )

        stream.stop_stream()
        stream.close()
        p.terminate()

    # ------------------ Grammar Correction ------------------ #
    def check_grammar(self):
        if not self.grammar_checkbox.isChecked():
            return

        text = self.text_box.toPlainText().strip()
        if not text:
            return

        try:
            response = requests.post(
                LANGUAGETOOL_URL,
                data={"language": "en-US", "text": text},
                timeout=3,
            )
            matches = response.json().get("matches", [])
            if matches:
                suggestions = []
                for match in matches[:3]:  # show top 3 corrections
                    msg = match.get("message", "")
                    repl = match.get("replacements", [])
                    if repl:
                        suggestions.append(f"{msg} → {repl[0]['value']}")
                if suggestions:
                    self.text_box.append("\n[Suggestions]: " + "; ".join(suggestions))
        except Exception as e:
            print("Grammar check failed:", e)

    # ------------------ Insert into Active Window ------------------ #
    def insert_text(self):
        text = self.text_box.toPlainText().strip()
        if text:
            subprocess.run(["xdotool", "type", text])

    # ------------------ Open Onboard Keyboard ------------------ #
    def open_keyboard(self):
        subprocess.Popen(["onboard"])


if _name_ == "_main_":
    app = QApplication(sys.argv)
    window = VoiceKeyboardApp()
    window.show()
    sys.exit(app.exec_())