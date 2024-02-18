from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Signal
import time
import sys
from PySide6.QtWidgets import QApplication
from Helpers.NestedNetworktableHelper import NestedNetworkTableManager


class MapDisplayWidget(QWidget):
    newCrosshairPosition = Signal(tuple)
    fieldX = 16.591788
    fieldY = 8.211312

    def __init__(self, alliance, parent=None):
        super().__init__(parent)

        self.mapLabel = QLabel()
        self.mapLabel.setScaledContents(True)

        self.mapPixmap = QPixmap("./Images/field24.png").scaled(600, 300)
        self.robotScale = 40
        self.robotPixmap = QPixmap("./Images/robot_frame.png").scaled(self.robotScale,
                                                                    self.robotScale)
        self.crosshairPixmap = QPixmap("./Images/crosshair.png")

        self.alliance = alliance

        if self.alliance == "red":
            rotationAngle = 90
        else:
            rotationAngle = -90
        transform = QTransform().rotate(rotationAngle)
        self.mapPixmap = self.mapPixmap.transformed(transform)

        # Set up QLabel for robot icon
        self.robotLabel = QLabel(self)
        self.robotLabel.setPixmap(self.robotPixmap)
        self.robotLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.robotLabel.setMask(self.robotPixmap.mask())  # Use transparency information for masking

        # Set up QLabel for crosshair (hide it for now)
        self.crosshairLabel = QLabel(self)
        self.crosshairLabel.setPixmap(self.crosshairPixmap)
        self.crosshairLabel.hide()
        self.crosshairLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed) \
 \
            # init crosshair position
        self.crosshairX = None
        self.crosshairY = None

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
        layout = QVBoxLayout()
        layout.addWidget(self.mapLabel)
        self.setLayout(layout)

    def changeAllianceColor(self, new_alliance_color):
        self.alliance = new_alliance_color
        self.reloadMaps()

    def reloadMaps(self):
        self.mapPixmap = QPixmap("./Images/field24.png").scaled(600, 300)
        rotation_angle = 90 if self.alliance == "red" else -90
        transform = QTransform().rotate(rotation_angle)
        self.mapPixmap = self.mapPixmap.transformed(transform)
        self.mapLabel.setPixmap(self.mapPixmap)

    def mousePressEvent(self, event):
        # Get the position of the mouse click
        position = event.pos()
        print(f"Clicked at position: {position.x()}, {position.y()}")
        self.crosshairLabel.hide()
        self.crosshairLabel.setGeometry(position.x() - 12, position.y() - 12, 25, 25)
        self.crosshairX = position.x()
        self.crosshairY = position.y()
        self.crosshairLabel.show()
        self.crosshairLabel.raise_()
        self.newCrosshairPosition.emit((self.crosshairX, self.crosshairY))

    def updateRobotPose(self, entryName, entryValue):
        self.robotLabel.hide()
        #type is tuple
        return
        print(entryValue)
        # print(range(len(entryValue)))
        for i in range(len(entryValue)):
            self.robotPose[i] = entryValue[i]
        # print(self.robotPose)
        newRobotPose = [self.robotPose[0] / self.fieldX * self.mapLabel.height(),
                        self.robotPose[1] / self.fieldY * self.mapLabel.width(),
                        self.robotPose[2]]
        #print(newRobotPose)
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
                int(self.mapLabel.width() - newRobotPose[1] - self.robotScale / 2 + 10),
                int(self.mapLabel.height() - newRobotPose[0] - self.robotScale / 2) + 10,
                self.robotScale,
                self.robotScale
            )
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
                int(newRobotPose[1] - self.robotScale / 2 + 10),
                int(newRobotPose[0] - self.robotScale / 2 + 10),
                self.robotScale,
                self.robotScale
            )
        self.robotLabel.show()
        self.robotLabel.raise_()
        self.robotLabel.raise_()
        #print(self.mapLabel.height())


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MapDisplayWidget('red')

    mw.show()
    sys.exit(app.exec())