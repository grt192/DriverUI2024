import sys
# PySide6 imports
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from Widgets.ControlWidget import ControlWidget
from Widgets.DriverCameraWidget import CameraWidget
from Widgets.MapDisplayWidget import MapDisplayWidget
from Widgets.SendCamIDWidget import SendCamIDWidget
from Widgets.RobotStatusWidget import RobotStatusWidget
from Widgets.PoseSwitchWidget import PoseSwitchWidget

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

        self.mapWidget = MapDisplayWidget(
            self.controlWidget.allianceToggle.currentText
        )
        self.mapWidget.setMaximumWidth(450)
        self.controlWidget.allianceToggle.toggled.connect(
            self.mapWidget.changeAllianceColor
        )

        self.mainLayout.addWidget(self.mapWidget)

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget = CameraWidget()
        self.cameraLayout.addWidget(self.cameraWidget)

        self.poseWidget = PoseSwitchWidget()
        self.poseWidget.setMaximumHeight(200)
        self.cameraLayout.addWidget(self.poseWidget)
        # print(self.cameraWidget.cameraDisplay.size())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
