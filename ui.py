from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen
import asyncio
import edge_tts
import threading
import tempfile
import os
from playsound import playsound


class RooneyUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Rooney AI")
        self.setGeometry(600, 300, 400, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.listening = False
        self.is_speaking = False   # 🔥 NEW FLAG

        self.status_label = QLabel("Waiting for wake word...", self)
        self.status_label.setStyleSheet("color: cyan; font-size: 16px;")
        self.status_label.move(90, 350)

        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(30)

    # 🔥 SPEAK FUNCTION WITH SPEAKING FLAG
    def speak(self, text):
        if not text:
            return

        clean_text = text.replace("\n", " ").strip()
        clean_text = clean_text[:1200]

        print("Speaking:", clean_text)

        self.is_speaking = True

        threading.Thread(target=self._speak_async, args=(clean_text,), daemon=True).start()

    def _speak_async(self, text):
        asyncio.run(self._generate_and_play(text))
        self.is_speaking = False   # 🔥 Re-enable listening after speaking

    async def _generate_and_play(self, text):
        communicate = edge_tts.Communicate(
            text=text,
            voice="en-US-AriaNeural"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_path = tmp_file.name

        await communicate.save(tmp_path)
        playsound(tmp_path)

        try:
            os.remove(tmp_path)
        except:
            pass

    def update_animation(self):
        self.angle += 3
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()

        if self.listening:
            color = QColor(0, 255, 255)
        else:
            color = QColor(0, 150, 255)

        pen = QPen(color, 4)
        painter.setPen(pen)

        painter.translate(center)
        painter.rotate(self.angle)
        painter.drawEllipse(-100, -100, 200, 200)