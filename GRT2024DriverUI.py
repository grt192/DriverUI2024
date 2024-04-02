import sys
# PySide6 imports
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, QEvent
from Widgets.ControlWidget import ControlWidget
from Widgets.DriverCameraWidget import CameraWidget
from Widgets.MapDisplayWidget import MapDisplayWidget
from Widgets.SendCamIDWidget import SendCamIDWidget
from Widgets.RobotStatusWidget import RobotStatusWidget
# from Widgets.PoseSwitchWidget import PoseSwitchWidget

class GRT2024DriverUI(QMainWindow):
    newCrosshairPosition = Signal(int, int)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("GRT 2024 Driver UI")
        self.resize(1920, 800)

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
        self.cameraLayout.addWidget(self.cameraWidget, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.pop_out_camera_button = QPushButton("Open Driver Camera in new window")
        self.pop_out_camera_button.clicked.connect(self.open_camera_window)
        self.cameraLayout.addWidget(self.pop_out_camera_button)

        # self.poseWidget = PoseSwitchWidget()
        # self.poseWidget.setMaximumHeight(200)
        # self.cameraLayout.addWidget(self.poseWidget)
        # print(self.cameraWidget.cameraDisplay.size())
        
    def open_camera_window(self):
        self.original_parent = self.cameraWidget.parent()
        self.cameraWidget.setParent(None)
        self.cameraWidget.show()
        self.cameraWidget.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Close:
            if obj == self.cameraWidget:
                self.cameraLayout.addWidget(self.cameraWidget, alignment=Qt.AlignmentFlag.AlignHCenter)
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.show()
    app.exec()
