from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QApplication
import sys
import os
from Helpers.NetworktableManager import NetworkTableManager
from Helpers.NestedNetworktableHelper import NestedNetworkTableManager


class MapDisplayWidget(QWidget):
    fieldX = 16.451
    fieldY = 8.211
    mapX = 300
    mapY = 606
    robotScale = 30

    def __init__(self, isRedAlliance, parent=None):
        super().__init__(parent)

        self.mapLabel = QLabel()
        self.mapLabel.setScaledContents(True)
        self.mapLabel.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.mapLabel.setMaximumWidth(self.mapX)
        self.mapLabel.setMaximumHeight(self.mapY)

        self.mapPixmap = QPixmap("./Images/Field.png")
        self.robotPixmap = QPixmap("./Images/Circle.jpg").scaled(
            self.robotScale,
            self.robotScale
            )
        self.shootPixmap = QPixmap("./Images/Circle.jpg").scaled(10, 10)
        self.shootLabel = QLabel(self.mapLabel)
        self.shootLabel.setPixmap(self.shootPixmap)
        self.isRedAllianceNTTable = NetworkTableManager("FMSInfo", "IsRedAlliance")
        self.isRedAllianceNTTable.new_value_available.connect(self.changeAllianceColor)
        self.isRedAlliance= self.isRedAllianceNTTable.getValue()
        print(self.isRedAllianceNTTable.getValue())

        if self.isRedAlliance:
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

        self.xShootNTManager = NetworkTableManager("Testing", "x", self)
        self.xShootNTManager.new_value_available.connect(self.updateShootingPose)
        self.yShootNTManager = NetworkTableManager("Testing", "y", self)
        self.yShootNTManager.new_value_available.connect(self.updateShootingPose)
        self.shootPose = [0., 0.]
        # Set up layout
        self.mapLabel.setPixmap(self.mapPixmap)
        layout = QVBoxLayout()
        layout.addWidget(self.mapLabel)
        self.setLayout(layout)

    def changeAllianceColor(self, info: tuple):
        print(info[1])
        if info[1]:
            self.alliance = "red"
        else:
            self.alliance = "blue"
        self.reloadMaps()

    def reloadMaps(self):
        self.mapPixmap = QPixmap("./Images/Field.png")
        rotation_angle = 180 if self.alliance == "red" else 0
        transform = QTransform().rotate(rotation_angle)
        self.mapPixmap = self.mapPixmap.transformed(transform)
        self.mapLabel.setPixmap(self.mapPixmap)

    def updateRobotPose(self, info: tuple):
        entryName = info[0]
        entryValue = info[1]
        if entryName == "position" and entryValue != None:
            self.robotPose[0] = entryValue
        elif entryName == "Robot" and entryValue != None:
            for i in range(1, len(entryValue)):
                self.robotPose[i] = entryValue[i]
        else:
            return
        # print(self.robotPose[2])
        self.robotLabel.hide()
        newRobotPose = [self.robotPose[0] / self.fieldX * self.mapY,
                        self.robotPose[1] / self.fieldY * self.mapX,
                        180 - self.robotPose[2]]
        if not self.isRedAlliance:
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
        # self.robotLabel.raise_()
        # self.robotLabel.raise_()

    def updateShootingPose(self, info):
        entryName = info[0]
        entryValue = info[1]
        # print(entryName)
        self.shootLabel.hide()
        if entryName == "/Testing/x":
            self.shootPose[0] = entryValue
        else:
            self.shootPose[1] = entryValue
        # print(self.shootPose)
        newShootPose = [self.shootPose[0] / self.fieldX * self.mapY,
                        self.shootPose[1] / self.fieldY * self.mapX]
        if not self.isRedAlliance:
           self.shootLabel.setGeometry(int(self.mapX - newShootPose[1] - 5), int(self.mapY - newShootPose[0] - 5), 10, 10)
        else:
            self.shootLabel.setGeometry(int(newShootPose[0])-5, int(newShootPose[1])-5, 10, 10)
        self.shootLabel.show()
        self.shootLabel.raise_()


    def printSize(self):
        print("Entire widget size:")
        print(self.size())
        print("Map label size:")
        print(self.mapLabel.size())
        print("Robot label size:")
        print(self.robotLabel.size())
        print("---------------------")