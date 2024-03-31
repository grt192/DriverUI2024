from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt
import requests
class ConnectionDisplayLabel(QLabel):

    def __init__(self, parameterName, url, parent = None):
        super().__init__(parameterName, parent)
        self.url = url
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.updateConnectionStatus()
    def updateConnectionStatus(self):
        try:
            response = requests.get(self.url, timeout=2)
            if response.status_code == 200:
                self.setStyleSheet(f"background-color: green;")
                self.setText("Connected")
            else:
                self.setStyleSheet(f"background-color: gray;")
                self.setText("Disconnected")
        except Exception as e:
            self.setStyleSheet(f"background-color: red;")
            self.setText("Disconnected")