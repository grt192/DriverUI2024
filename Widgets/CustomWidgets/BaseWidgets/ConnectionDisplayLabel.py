from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt, QTimer
import requests
class ConnectionDisplayLabel(QLabel):

    def __init__(
        self, parameterName, url,
        trueColor: tuple, falseColor: tuple,
        generalStyleSheet: str = "color: white; font-weight: bold; font-size: 30px;",
        parent = None
    ):
        super().__init__(parameterName, parent)
        self.parameterName = parameterName
        self.url = url
        self.generalStyleSheet = generalStyleSheet
        self.trueColor = trueColor
        self.falseColor = falseColor
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.updateConnectionStatus()
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.updateConnectionStatus)
        # self.timer.start(1000)
    def updateConnectionStatus(self):
        try:
            response = requests.get(self.url, timeout=2)
            if response.status_code == 200:
                self.setStyleSheet("background-color: rgb" + str(self.trueColor) + ";" + self.generalStyleSheet)
                self.setText(self.parameterName + " Connected")
            else:
                self.setStyleSheet(f"background-color: rgb" + str(self.falseColor) + ";" + self.generalStyleSheet)
                self.setText(str(response.status_code) + " Disconnected")
        except Exception as e:
            self.setStyleSheet(f"background-color: rgb" + str(self.falseColor) + ";" + self.generalStyleSheet)
            self.setText(str(e))