import sys
# PySide6 imports
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QVBoxLayout
from Widgets.InfoWidget import InfoWidget
from Widgets.InfoWidget2 import InfoWidget2
from Widgets.DriverCameraWidget import CameraWidget
from Widgets.MapDisplayWidget import MapDisplayWidget

class GRT2024DriverUI(QMainWindow):
    newCrosshairPosition = Signal(int, int)

    def __init__(self):
        super().__init__()

        self.setWindowTitle("GRT 2024 Driver UI")
        self.resize(1920, 630)
        self.setMaximumHeight(630)
        self.mainLayout = QHBoxLayout()

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.mainLayout)

        self.FMSInfoWidget = InfoWidget()
        self.FMSInfoWidget.setMaximumWidth(200)
        self.mainLayout.addWidget(self.FMSInfoWidget)

        self.mapWidget = MapDisplayWidget(self.FMSInfoWidget.allianceLabel.isRedAlliance, self)
        self.mapWidget.setMaximumWidth(300)
        self.mapWidget.setMaximumHeight(606)
        self.FMSInfoWidget.allianceLabel.isRedSignal.connect(self.mapWidget.changeAllianceColor)

        self.mainLayout.addWidget(self.mapWidget)

        self.cameraLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.cameraLayout)

        self.cameraWidget = CameraWidget()
        self.cameraLayout.addWidget(self.cameraWidget)

        self.infoWidget2 = InfoWidget2()
        self.infoWidget2.setMaximumWidth(250)
        self.mainLayout.addWidget(self.infoWidget2)
        self.setStyleSheet("background-color: black; color: white;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GRT2024DriverUI()
    window.showFullScreen()
    window.setGeometry(0, 0, 1920, 780)
    app.exec()
