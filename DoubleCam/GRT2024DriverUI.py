import sys
# PySide6 imports
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Helpers.NetworktableHelper import NetworkTableManager
from Widgets.ControlWidget import ControlWidget
from Widgets.MapWidget import MapWidget
from Widgets.DriverCameraWidget import CameraWidget
from Widgets.ToggleWidget import ToggleWidget


class GRT2024DriverUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GRT 2024 Driver UI")
        self.resize(1920, 1080)

        self.mainLayout = QHBoxLayout()

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.mainLayout)

        self.controlWidget = ControlWidget()
        self.controlWidget.setMaximumWidth(200)
        self.mainLayout.addWidget(self.controlWidget)

        self.mapWidget = MapWidget(
            self.controlWidget.allianceToggle.currentText
        )
        self.controlWidget.allianceToggle.toggled.connect(
            self.mapWidget.changeAllianceColor
        )
        self.mainLayout.addWidget(self.mapWidget)

        self.sendDestinationWidget = ToggleWidget(
            "Send Destination", "", "", ("Send", "Sending...")
        )
        self.sendDestinationWidget.setMaximumWidth(100)
        self.mainLayout.addWidget(self.sendDestinationWidget)

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget1 = CameraWidget()
        self.cameraWidget2 = CameraWidget()
        self.cameraLayout.addWidget(self.cameraWidget1)
        self.cameraLayout.addWidget(self.cameraWidget2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
