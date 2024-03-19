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
        self.robotPixmap = QPixmap("./Images/Robot.png").scaled(self.robotScale,
                                                                    self.robotScale)

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


        self.robotPoseRootNTTableName = "Shuffleboard"
        self.robotPoseNTTableNames = ["Auton", "Field"]
        self.robotPoseNTManager = NestedNetworkTableManager(
            self.robotPoseRootNTTableName,
            self.robotPoseNTTableNames, "Robot"
        )
        self.robotPoseNTManager.new_value_available.connect(self.updateRobotPose)
        self.robotPose = [0., 0., 0.]
        # Set up layout
        self.mapLabel.setPixmap(self.mapPixmap)
        print(self.mapLabel.size())
        layout = QVBoxLayout()
        layout.addWidget(self.mapLabel)
        self.setLayout(layout)
        # print(self.mapLabel.size())
        self.updateRobotPose("pose", (3,0,0))
        self.printSize()

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
        print(entryValue)
        self.robotLabel.hide()
        for i in range(len(entryValue)):
            self.robotPose[i] = entryValue[i]
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
                int(newRobotPose[1] - self.robotScale / 2 ),
                int(newRobotPose[0] - self.robotScale / 2 ),
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

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MapDisplayWidget('red')

    mw.show()
    sys.exit(app.exec())