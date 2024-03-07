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

        self.mapWidget = MapDisplayWidget(
            self.controlWidget.allianceToggle.currentText
        )
        self.mapWidget.setContentsMargins(0,0,0,0)
        self.mapWidget.setMaximumHeight(800)
        self.mapWidget.setMaximumWidth(400)
        self.controlWidget.allianceToggle.toggled.connect(
            self.mapWidget.changeAllianceColor
        )

        self.mainLayout.addWidget(self.mapWidget)
        print("Created mapLayout")

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget1 = CameraWidget("Camera1")
        print("Created cameraWidget1")
        self.cameraLayout.addWidget(self.cameraWidget1)
        self.robotStatusLayout = QHBoxLayout()
        self.frontSensorWidget = RobotStatusWidget("Front Sensor", "RobotStatus", "frontSensor")
        self.frontSensorWidget.setMinimumHeight(200)
        self.robotStatusLayout.addWidget(self.frontSensorWidget)
        self.backSensorWidget = RobotStatusWidget("Back Sensor", "RobotStatus", "backSensor")
        self.backSensorWidget.setMinimumHeight(200)
        self.robotStatusLayout.addWidget(self.backSensorWidget)
        self.shooterReadyWidget = RobotStatusWidget("Shooter Ready", "RobotStatus", "shooterReady")
        self.shooterReadyWidget.setMinimumHeight(200)
        self.robotStatusLayout.addWidget(self.shooterReadyWidget)
        self.noteDetectedWidget = RobotStatusWidget("Note Detected", "Vision", "noteDetected")
        self.noteDetectedWidget.setMinimumHeight(200)
        self.robotStatusLayout.addWidget(self.noteDetectedWidget)
        self.cameraLayout.addLayout(self.robotStatusLayout)

        # self.sendCamIDWidget = SendCamIDWidget("Switch", "camera", "id")
        # self.cameraLayout.addWidget(self.sendCamIDWidget)
        # print("Created cameraLayout")







if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
