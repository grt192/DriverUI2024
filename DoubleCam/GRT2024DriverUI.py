import sys
# PySide6 imports
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from Widgets.ControlWidget import ControlWidget
from Widgets.DriverCameraWidget import CameraWidget
from Widgets.MapWidget import MapWidget
from Widgets.SendCamIDWidget import SendCamIDWidget


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
        self.controlWidget.setMaximumWidth(130)
        self.mainLayout.addWidget(self.controlWidget)

        self.mapWidget = MapWidget(
            self.controlWidget.allianceToggle.currentText
        )
        self.controlWidget.allianceToggle.toggled.connect(
            self.mapWidget.changeAllianceColor
        )
        self.mapLayout = QVBoxLayout()
        self.mapLayout.addWidget(self.mapWidget)

        self.mainLayout.addLayout(self.mapLayout)

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget1 = CameraWidget("Camera1")
        self.cameraWidget1.setMaximumWidth(832)
        self.cameraWidget1.setMaximumHeight(400)
        self.cameraLayout.addWidget(self.cameraWidget1)
        self.sendCamIDWidget = SendCamIDWidget("Switch", "camera", "id")
        self.cameraLayout.addWidget(self.sendCamIDWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
