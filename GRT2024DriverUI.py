import sys
# PySide6 imports
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from Widgets.FMSInfoWidget import FMSInfoWidget
from Widgets.DriverCameraWidget import CameraWidget
from Widgets.MapDisplayWidget import MapDisplayWidget
from Widgets.SendCamIDWidget import SendCamIDWidget
from Widgets.RobotStatusWidget import RobotStatusWidget

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

        self.FMSInfoWidget = FMSInfoWidget()
        self.FMSInfoWidget.setMaximumWidth(200)
        self.mainLayout.addWidget(self.FMSInfoWidget)

        self.mapWidget = MapDisplayWidget(
            self.FMSInfoWidget.isRedAlliance
        )
        self.mapWidget.setMaximumWidth(450)

        self.mainLayout.addWidget(self.mapWidget)

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget = CameraWidget()
        self.cameraLayout.addWidget(self.cameraWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
