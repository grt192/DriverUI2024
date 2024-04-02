from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QApplication
import sys
import os
from Helpers.NestedNetworktableHelper import NestedNetworkTableManager


class MapDisplayWidget(QWidget):
    newCrosshairPosition = Signal(tuple)
    fieldX = 16.451
    fieldY = 8.211
    mapX = 400
    mapY = 801
    robotScale = 50

    def __init__(self, alliance, parent=None):
        super().__init__(parent)

        self.mapLabel = QLabel()
        self.mapLabel.setScaledContents(True)
        self.mapLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.mapLabel.setMaximumWidth(self.mapX)
        self.mapLabel.setMaximumHeight(self.mapY)

        self.mapPixmap = QPixmap("./Images/Field.png")
        self.robotPixmap = QPixmap("./Images/Robot.png").scaled(
            self.robotScale,
            self.robotScale
            )

        self.alliance = alliance

        if self.alliance == "red":
            rotationAngle = 180
        else:
            rotationAngle = 0
        transform = QTransform().rotate(rotationAngle)
        self.mapPixmap = self.mapPixmap.transformed(transform)

        # Set up QLabel for robot icon
        self.robotLabel = QLabel(self.mapLabel)
        self.robotLabel.setPixmap(self.robotPixmap)
        self.robotLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.robotLabel.setMask(self.robotPixmap.mask())  # Use transparency information for masking

        self.robotPoseNTTableNames = ["Shuffleboard", "Auton", "Field"]
        self.robotPoseNTManager = NestedNetworkTableManager(self.robotPoseNTTableNames,"Robot")
        self.robotPoseNTManager.new_value_available.connect(self.updateRobotPose)

        self.xPoseNTTableNames = ["Shuffleboard", "Auton"]
        self.xPoseNTManager = NestedNetworkTableManager(self.xPoseNTTableNames,"position")
        self.xPoseNTManager.new_value_available.connect(self.updateRobotPose)
        self.robotPose = [0., 0., 0.]

        # Set up layout
        self.mapLabel.setPixmap(self.mapPixmap)
        layout = QVBoxLayout()
        layout.addWidget(self.mapLabel)
        self.setLayout(layout)

    def changeAllianceColor(self, new_alliance_color):
        self.alliance = new_alliance_color
        self.reloadMaps()

    def reloadMaps(self):
        self.mapPixmap = QPixmap("./Images/Field.png")
        rotation_angle = 180 if self.alliance == "red" else 0
        transform = QTransform().rotate(rotation_angle)
        self.mapPixmap = self.mapPixmap.transformed(transform)
        self.mapLabel.setPixmap(self.mapPixmap)

    def updateRobotPose(self, entryName, entryValue):
        if entryName == "position" and entryValue != None:
            print("position")
            self.robotPose[0] = entryValue
        elif entryName == "Robot" and entryValue != None:
            for i in range(1, len(entryValue)):
                self.robotPose[i] = entryValue[i]
            print("Robot")
        else:
            return
        self.robotLabel.hide()
        newRobotPose = [self.robotPose[0] / self.fieldX * self.mapY,
                        self.robotPose[1] / self.fieldY * self.mapX,
                        180 - self.robotPose[2]]
        if self.alliance == "blue":
            self.robotLabel.setPixmap(
                self.robotPixmap.scaled(
                    self.robotScale,
                    self.robotScale,
                ).transformed(
                    QTransform().rotate(newRobotPose[2])
                )
            )
            self.robotLabel.setGeometry(
                int(self.mapX - newRobotPose[1] - self.robotScale / 2),
                int(self.mapY - newRobotPose[0] - self.robotScale / 2),
                self.robotScale,
                self.robotScale
            )
            # print(int(self.mapX - newRobotPose[1] - self.robotScale / 2))
            # print(int(self.mapY - newRobotPose[0] - self.robotScale / 2))
            # print("-----------------------")
        else:
            self.robotLabel.setPixmap(
                self.robotPixmap.scaled(
                    self.robotScale,
                    self.robotScale,
                ).transformed(
                    QTransform().rotate(newRobotPose[2] - 180)
                )
            )
            self.robotLabel.setGeometry(
                int(newRobotPose[1] - self.robotScale / 2),
                int(newRobotPose[0] - self.robotScale / 2),
                self.robotScale,
                self.robotScale
            )
        self.robotLabel.show()
        self.robotLabel.raise_()
        self.robotLabel.raise_()

    def printSize(self):
        print("Entire widget size:")
        print(self.size())
        print("Map label size:")
        print(self.mapLabel.size())
        print("Robot label size:")
        print(self.robotLabel.size())
        print("---------------------")