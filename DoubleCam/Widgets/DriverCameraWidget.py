import sys
import time
from PySide6 import QtCore
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtWidgets import QApplication, QSizePolicy
from PySide6.QtGui import QImage, QPixmap
import numpy as np
from time import perf_counter
import cv2
import requests
from Helpers.NetworktableHelper import NetworkTableManager
from threading import *


class CameraWidget(QWidget):
    visionURL = "http://10.1.92.19:1186/stream.mjpg"
    visionTestURL = "http://10.1.92.19:1186"
    camURl = "http://10.1.92.2:1181/stream.mjpg"
    camTestURL = "http://10.1.92.2:1181"
    vision = False
    driverCamWidth = 176
    driverCamHeight = 144
    def __init__(self, displayName='GRT Driver Cam', parent=None):
        super(CameraWidget, self).__init__(parent)

        self.cameraDisplay = QLabel(self)
        self.cameraDisplay.setScaledContents(True)
        self.cameraDisplay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cameraDisplay.setMaximumWidth(3 * self.driverCamWidth)
        self.cameraDisplay.setMaximumHeight(3 * self.driverCamHeight)
        print("Created cameraDisplay label")

        #listen to elevator state change
        self.elevatorPositionNTManager = NetworkTableManager("elevator", "position")
        self.elevatorPositionNTManager.new_value_available.connect(self.switchBasedOnElevatorPosition)
        print("Created NTManager")

        # Check if network is available
        self.is_network_available = self.checkNetwork()
        print("runned is_network_available")
        # return
        if self.is_network_available:
            try:
                self.setDriverCap()
                self.setVisionCap()
            except Exception as e:
                print(e)
        else:
            self.cameraDisplay.setText("Unable to access cameras")
        print("Created video caps")
        #use this time to call the DisplayStream method to retrieve and display frames.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayStream)
        self.timer.setSingleShot(True)
        self.timer.start(1)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)
        self.vtimer = QtCore.QTimer()
        self.vtimer.timeout.connect(self.captureVision)
        self.vtimer.setSingleShot(True)
        self.vtimer.start(1)
        self.reconnectButton = QPushButton("Reconnect")
        self.reconnectButton.clicked.connect(self.reconnect)

        self.switchToDriverButton = QPushButton("Driver")
        self.switchToDriverButton.clicked.connect(self.switchToDriverCam)

        self.switchToVisionButton = QPushButton("Vision")
        self.switchToVisionButton.clicked.connect(self.switchToVisionCam)

        self.switchWidget = QWidget()
        self.switchLayout = QHBoxLayout(self)
        self.switchLayout.addWidget(self.reconnectButton)
        self.switchLayout.addWidget(self.switchToDriverButton)
        self.switchLayout.addWidget(self.switchToVisionButton)
        self.switchWidget.setLayout(self.switchLayout)
        print("Created reconnect button")

        layout = QVBoxLayout(self)

        #Add everything layout.
        layout.addWidget(self.cameraDisplay)
        layout.addWidget(self.switchWidget)
        self.setLayout(layout)
    def setVisionCap(self):
        self.visionCap = cv2.VideoCapture(self.visionURL)
        self.visionCap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.visionCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.visionCap.set(cv2.CAP_PROP_FPS, 30)
        self.visionCap.set(cv2.CAP_PROP_EXPOSURE, 0.5)
    def setDriverCap(self):
        self.driverCap = cv2.VideoCapture(self.camURl)
        self.driverCap.set(cv2.CAP_PROP_FRAME_WIDTH, 176)
        self.driverCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)
        self.driverCap.set(cv2.CAP_PROP_FPS, 60)
        self.driverCap.set(cv2.CAP_PROP_EXPOSURE, 0.5)
    def reconnect(self):
        if self.checkDriver():
            self.setDriverCap()
            self.timer.start(1)
        if self.checkVision():
            self.setVisionCap()
            self.vtimer.start(1)
        else:
           print("Network Issue!")
    def checkVision(self):
        try:
            response = requests.get(self.visionTestURL, timeout=1)
            if response.status_code != 200:
                print("Vision not accessable! Status Code: " + str(response.status_code))
                return False
            response.close()
        except Exception as e:
            print("Check Netowrk exception")
            print(e)
        return True
    def checkDriver(self):
        try:
            response = requests.get(self.camTestURL, timeout=1)
            if response.status_code != 200:
                print("Driver cam not accessable! Status Code: " + str(response.status_code))
                return False
            response.close()
        except Exception as e:
            print("Check Netowrk exception")
            print(e)
        return True
    def checkNetwork(self):
        return self.checkVision() and self.checkDriver()
    def switchBasedOnElevatorPosition(self, position):
        #type of position is tuple
        if position[1] == 0.:
            print("is 0")
            self.switchToDriverCam()
        elif position[1] == 3.:
            print("is 3")
            self.switchToVisionCam()
    def switchToVisionCam(self):
        print("switch to vision")
        self.vision = True
        self.vtimer.start(1)
    def switchToDriverCam(self):
        print("switch to driver")
        self.vision = False
        self.timer.start(1)
    def captureVision(self):
        print("Capture Vision")
        if not self.checkVision():
            return
        elif not self.visionCap.isOpened():
            print("Can't access vision camera")
            return
        elif self.vision:
            vret, vframe = self.visionCap.read()
            if self.vision:
                vframe = cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB)
                h, w, ch = vframe.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(
                    vframe.data, w, h, bytes_per_line, QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(convert_to_Qt_format)
                self.cameraDisplay.setPixmap(pixmap)
                self.vtimer.start(1)
    def displayStream(self):
        print("Display Stream")
        if not self.checkDriver():
            return
        elif not self.driverCap.isOpened():
            print("Can't access driver camera")
            return
        elif not self.vision:
            ret, frame = self.driverCap.read()
            if not self.vision:
                # Convert the image to Qt format
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytesPerLine = ch * w
                cvtToQtFormat = QImage(
                    frame.data, w, h, bytesPerLine, QImage.Format_RGB888
                )
                pixmap = QPixmap.fromImage(cvtToQtFormat)
                self.cameraDisplay.setPixmap(pixmap)
                self.timer.start(1)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = CameraWidget()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec())
