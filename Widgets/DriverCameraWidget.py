import sys
from PySide6 import QtCore
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QApplication, QSizePolicy
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
import cv2
import requests


class CameraWidget(QWidget):
    camURl = "http://10.1.92.2:1181/stream.mjpg"
    camTestURL = "http://10.1.92.2:1181"
    resolutionX = 176
    resolutionY = 144
    FPS = 30
    scale = 2
    driverCamWidth = 320 * scale
    driverCamHeight = 240 * scale
    xScale = 1.5
    windowHeight = 300
    windowWidth = driverCamWidth * xScale
    def __init__(self, displayName='GRT Driver Cam', parent=None):
        super(CameraWidget, self).__init__(parent)

        self.cameraDisplay = QLabel(self)
        self.cameraDisplay.setScaledContents(True)
        self.cameraDisplay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cameraDisplay.setMaximumWidth(800)
        self.cameraDisplay.setMaximumHeight(400)
        print("Created cameraDisplay label")

        #use this time to call the DisplayStream method to retrieve and display frames.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayStream)
        self.timer.setSingleShot(True)

        if self.checkDriver():
            self.setDriverCap()
            self.timer.start(1)

        self.reconnectButton = QPushButton("Reconnect")
        self.reconnectButton.clicked.connect(self.reconnect)
        print("Created reconnect button")

        layout = QVBoxLayout(self)

        #Add everything layout.
        layout.addWidget(self.cameraDisplay)
        layout.addWidget(self.reconnectButton)
        self.setLayout(layout)

    def setDriverCap(self):
        self.driverCap = cv2.VideoCapture(self.camURl)
        self.driverCap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolutionX)
        self.driverCap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolutionY)
        self.driverCap.set(cv2.CAP_PROP_FPS, self.FPS)
        # self.driverCap.set(cv2.CAP_PROP_EXPOSURE, 0.5)
        # self.driverCap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
    def reconnect(self):
        if self.checkDriver():
            self.setDriverCap()
            self.timer.start(1)
        else:
           print("Network Issue!")
    def checkDriver(self):
        try:
            response = requests.get(self.camTestURL, timeout=1)
            if response.status_code != 200:
                print("Driver cam not accessable! Status Code: " + str(response.status_code))
                return False
            response.close()
        except Exception as e:
            print("Check Driver exception in the following line:")
            print(e)
            return False
        return True
    def displayStream(self):
        if not self.checkDriver():
            return
        elif not self.driverCap.isOpened():
            print("Can't access driver camera")
            return
        else:
            ret, frame = self.driverCap.read()
            # Convert the image to Qt format
            frame = cv2.flip(frame, flipCode=-1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            cvtToQtFormat = QImage(
                frame.data, w, h, bytesPerLine, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(cvtToQtFormat)
            self.cameraDisplay.setPixmap(pixmap)
            # self.cameraDisplay.resize(800,self.windowHeight)
            self.cameraDisplay.setAlignment(Qt.AlignCenter)
            # self.setDriverCap()
            self.timer.start(1)