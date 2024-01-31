import sys
# PySide6 imports
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from Helpers.NetworktableHelper import NetworkTableManager
from Widgets.ControlWidget import ControlWidget
from Widgets.MapDisplayWidget import MapDisplayWidget
from Widgets.DriverCameraWidget import CameraWidget
from Widgets.ToggleWidget import ToggleWidget
from Widgets.MapWidget import MapWidget
from Widgets.SendIncreaseIntWidget import SendIncreaseIntWidget


class GRT2024DriverUI(QMainWindow):
    newCrosshairPosition = Signal(int, int)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("GRT 2024 Driver UI")
        self.resize(1920, 1080)

        self.mainLayout = QHBoxLayout()

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.mainLayout)

        self.controlWidget = ControlWidget()
        self.controlWidget.setMaximumWidth(100)
        self.mainLayout.addWidget(self.controlWidget)

        self.mapWidget = MapWidget(
            self.controlWidget.allianceToggle.currentText
        )
        self.controlWidget.allianceToggle.toggled.connect(
            self.mapWidget.changeAllianceColor
        )
        self.mapLayout = QVBoxLayout()
        self.mapLayout.addWidget(self.mapWidget)
        self.alignLayout = QHBoxLayout()
        self.sourceAlignWidget = SendIncreaseIntWidget(
            "Source", "Alignment", "Source", self
        )
        self.alignLayout.addWidget(self.sourceAlignWidget)
        self.ampAlignWidget = SendIncreaseIntWidget(
            "AMP", "Alignment", "AMP", self
        )
        self.alignLayout.addWidget(self.ampAlignWidget)
        self.speakerAlignWidget = SendIncreaseIntWidget(
            "Speaker", "Alignment", "Speaker", self
        )
        self.alignLayout.addWidget(self.speakerAlignWidget)
        self.mapLayout.addLayout(self.alignLayout)
        self.mainLayout.addLayout(self.mapLayout)

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget1 = CameraWidget("Camera1")
        self.cameraWidget1.setMaximumWidth(832)
        self.cameraWidget1.setMaximumHeight(480)
        self.cameraLayout.addWidget(self.cameraWidget1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
