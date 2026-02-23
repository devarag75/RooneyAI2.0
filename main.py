import sys
import threading
from PyQt5.QtWidgets import QApplication
from ui import RooneyUI
from voice import start_voice

app = QApplication(sys.argv)

window = RooneyUI()
window.show()

voice_thread = threading.Thread(target=start_voice, args=(window,))
voice_thread.daemon = True
voice_thread.start()

sys.exit(app.exec_())