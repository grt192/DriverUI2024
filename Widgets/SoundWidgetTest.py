import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QSoundEffect

class SoundWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.sound_button = QPushButton("Play Sound")
        self.sound_button.clicked.connect(self.play_sound)

        layout.addWidget(self.sound_button)

        self.setLayout(layout)
        self.setWindowTitle("Sound Widget")

        self.sound_effect = QSoundEffect(self)
        self.sound_effect.setSource(QUrl.fromLocalFile("explosion_sound.wav"))  # Change this to your sound file path

    def play_sound(self):
        self.sound_effect.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = SoundWidget()
    widget.show()
    sys.exit(app.exec())
