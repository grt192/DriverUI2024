import sys
import time
from PySide6 import QtCore
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout
from PySide6.QtWidgets import QApplication, QSizePolicy
from PySide6.QtGui import QImage, QPixmap
import numpy as np
from time import perf_counter
import cv2
import requests
from Helpers.NetworktableHelper import NetworkTableManager
from threading import *


class CameraWidget(QWidget):
    visionURL = "http://photonvision.local:1186/stream.mjpg"
    visionTestURL = "http://photonvision.local:1186"
    camURl = "http://10.1.92.2:1181/stream.mjpg"
    camTestURL = "http://10.1.92.2:1181"
    vision = False
    driverCamWidth = 176
    driverCamHeight = 144
    def __init__(self, displayName='GRT Driver Cam', parent=None):
        super(CameraWidget, self).__init__(parent)

        self.cameraDisplay = QLabel(self)
        self.cameraDisplay.setScaledContents(True)
        self.cameraDisplay.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.cameraDisplay.setMaximumWidth(3 * self.driverCamWidth)
        self.cameraDisplay.setMaximumHeight(3 * self.driverCamHeight)
        print("Created cameraDisplay label")

        #listen to elevator state change
        self.elevatorPositionNTManager = NetworkTableManager("elevator", "position")
        self.elevatorPositionNTManager.new_value_available.connect(self.switchBasedOnElevatorPosition)
        print("Created NTManager")

        # Check if network is available
        self.is_network_available = self.check_network()
        self.endTime = time.time()
        self.duration = self.endTime - self.startTime
        print("Duration: " + str(self.duration))
        print("runned is_network_available")
        return
        if self.is_network_available:
            try:
                self.driverCap = cv2.VideoCapture(self.camURl)
                self.driverCap.set(cv2.CAP_PROP_FRAME_WIDTH, 176)
                self.driverCap.set(cv2.CAP_PROP_FRAME_HEIGHT, 144)
                self.visionCap = cv2.VideoCapture(self.visionURL)
            except Exception as e:
                print(e)
        else:
            self.cameraDisplay.setText("Unable to access cameras")
        print("Created video caps")
        #use this time to call the DisplayStream method to retrieve and display frames.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayStream)
        self.timer.start(1)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)
        self.vtimer = QtCore.QTimer()
        self.vtimer.timeout.connect(self.captureVision)
        self.vtimer.start(1)
        self.cnt = 0
        self.reconnectButton = QPushButton("Reconnect")
        self.reconnectButton.clicked.connect(self.reconnect)
        print("Created reconnect button")

        layout = QVBoxLayout(self)

        #Add everything layout.
        layout.addWidget(self.cameraDisplay)
        layout.addWidget(self.reconnectButton)


    def reconnect(self):
        self.driverCap = cv2.VideoCapture(self.camURl)
        self.visionCap = cv2.VideoCapture(self.visionURL)
        print("reconnect finished")
    def check_network(self):
        # Check if network is available
        self.startTime = time.time()
        try:
            response = requests.get(self.visionTestURL, timeout=1)
            if response.status_code != 200:
                print("Vision not accessable! Status Code: " + str(response.status_code))
                return False
            response.close()
            response = requests.get(self.camTestURL, timeout=1)
            if response.status_code != 200:
                print("Driver cam not accessable! Status Code: " + str(response.status_code))
                return False
            response.close()
        except Exception as e:
            print(e)
            return False
        return True
    def switchBasedOnElevatorPosition(self, position):
        #type of position is tuple
        #print(type(position))
        # print(type(position[1]))
        # print(position[1])
        if position[1] == 0.:
            print("is 0")
            self.switchToDriverCam()
        elif position[1] == 3.:
            print("is 3")
            self.switchToVisionCam()
    def switchToVisionCam(self):
        print("switch to vision")
        self.vision = True
    def switchToDriverCam(self):
        print("switch to driver")
        self.vision = False
    def captureVision(self):
        self.visionCap.grab()
        self.visionCap.grab()
        vret, vframe = self.visionCap.read()
        if vret and self.vision:
            vframe = cv2.cvtColor(vframe, cv2.COLOR_BGR2RGB)
            h, w, ch = vframe.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(
                vframe.data, w, h, bytes_per_line, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.cameraDisplay.setPixmap(pixmap)
            # self.endTime = time.time()
            # print(self.endTime-self.startTime)
            self.vtimer.start()
            self.cnt += 1
            # self.startTime = time.time()
    def displayStream(self):
        self.driverCap.grab()
        self.driverCap.grab()
        if self.cnt > 600:
            #self.reconnect()
            cnt = 0
        ret, frame = self.driverCap.read()
        if ret and not self.vision:
            # print("got new frame")
            # Convert the image to Qt format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(
                frame.data, w, h, bytes_per_line, QImage.Format_RGB888
                )
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.cameraDisplay.setPixmap(pixmap)
            #self.endTime = time.time()
            #print(self.endTime-self.startTime)
            self.timer.start()
            self.cnt += 1
            #self.startTime = time.time()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = CameraWidget()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec())
