from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt, QTimer
from Helpers.NetworktableManager import NetworkTableManager
from Helpers.NestedNetworktableHelper import NestedNetworkTableManager

class TranslationalSpeedLabel(QLabel):

    def __init__(self, timer: QTimer, parent = None):
        super().__init__("T Speed", parent)

        self.robotPoseNTTableNames = ["Shuffleboard", "Auton", "Field"]
        self.robotPoseNTManager = NestedNetworkTableManager(
            self.robotPoseNTTableNames, "Robot"
        )
        self.xPoseNTTableNames = ["Shuffleboard", "Auton"]
        self.xPoseNTManager = NestedNetworkTableManager(
            self.xPoseNTTableNames, "position"
        )
        self.timer = timer
        self.timer.timeout.connect(self.updateFromNT)

        self.robotPose = [0., 0., 0.]
        self.speed = 0
        self.setStyleSheet(f"background-color: black; color: red;")
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)

    def getPose(self):
        self.robotPose = list(self.robotPoseNTManager.getValue())
        self.robotPose[0] = self.xPoseNTManager.getValue()
    def updateFromNT(self):
        oldRobotPose = self.robotPose
        self.getPose()
        xDiff = self.robotPose[0] - oldRobotPose[0]
        yDiff = self.robotPose[1] - oldRobotPose[1]
        rDiff = (xDiff ** 2 + yDiff ** 2) ** 0.5
        speed = rDiff / 0.1
        acceleration = (speed - self.speed) / 0.1
        self.speed = speed
        self.setText(
            "v: " + str("{:.2f}".format(speed)) +
            " a: " + "{:.2f}".format(acceleration)
        )
