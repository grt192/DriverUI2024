import sys
# PySide6 imports
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout

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
        print("Created controlWidget")

        self.mapWidget = MapWidget(
            self.controlWidget.allianceToggle.currentText
        )
        self.controlWidget.allianceToggle.toggled.connect(
            self.mapWidget.changeAllianceColor
        )
        self.mapLayout = QVBoxLayout()
        self.mapLayout.addWidget(self.mapWidget)

        self.mainLayout.addLayout(self.mapLayout)
        print("Created mapLayout")

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget1 = CameraWidget("Camera1")
        print("Created cameraWidget1")
        self.cameraLayout.addWidget(self.cameraWidget1)
        self.sendCamIDWidget = SendCamIDWidget("Switch", "camera", "id")
        self.cameraLayout.addWidget(self.sendCamIDWidget)
        print("Created cameraLayout")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
