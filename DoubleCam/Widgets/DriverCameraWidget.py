import sys
import time
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import numpy as np
from time import perf_counter
import cv2
import requests
from Helpers.NetworktableHelper import NetworkTableManager
from threading import *


class CameraWidget(QWidget):
    visionURL = "http://photonvision.local:1186/stream.mjpg"
    cam1URl = "http://10.1.92.2:1181/stream.mjpg"
    vision = False
    def __init__(self, displayName='GRT Driver Cam', parent=None):
        super(CameraWidget, self).__init__(parent)

        self.displayName = QLabel(displayName)
        self.displayName.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        self.cameraDisplay = QLabel()
        self.cameraDisplay.setScaledContents(True)
        self.cameraDisplay.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.cameraDisplay.setMaximumWidth(528)
        self.cameraDisplay.setMaximumHeight(432)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        #listen to elevator state change
        self.elevatorPositionNTManager = NetworkTableManager("elevator", "position")
        self.elevatorPositionNTManager.new_value_available.connect(self.switchBasedOnElevatorPosition)

        if displayName == "Camera1":
            self.URL = "http://10.1.92.2:1181/stream.mjpg"
            self.TEST_URL = "http://10.1.92.2:1181"
        elif displayName == "Camera2":
            self.URL = "http://10.1.92.2:1182/stream.mjpg"
            self.TEST_URL = "http://10.1.92.2:1182"
        # Check if network is available
        self.is_network_available = self.check_network()

        if self.is_network_available:

            #init url, response, and byte stream.
            self.url = self.URL
            try:
                self.cap = cv2.VideoCapture(self.url)
                self.driverCap = cv2.VideoCapture(self.url)
                self.visionCap = cv2.VideoCapture("http://photonvision.local:1186/stream.mjpg")
            except Exception as e:
                print(e)
        else:
            self.url = None
            return
        #use this time to call the DisplayStream method to retrieve and display frames.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayStream)
        self.timer.start(1)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)
        #self.startTime = time.time()
        self.cnt = 0

        #FPS calculation
        self.actual_fps = 0
        self.past_five_instantaneous_fps = [0, 0, 0, 0, 0]
        self.updateTime = perf_counter()
        self.elapsed = 0
        #self.time_old = time.time()

        self.reconnectButton = QPushButton("Reconnect")
        self.reconnectButton.clicked.connect(self.reconnect)

        layout = QVBoxLayout(self)

        #Add everything layout.
        layout.addWidget(self.displayName)
        layout.addWidget(self.cameraDisplay)
        layout.addWidget(self.reconnectButton)


    def reconnect(self):
        self.cap.release()
        self.cnt = 0
        self.cap = cv2.VideoCapture(self.url)
        print("reconnect finished")
    def check_network(self):
        # Check if network is available
        try:
            response = requests.get(self.TEST_URL, timeout=2)
            if response.status_code == 200:
                response.close()
                return True
            else:
                print(response.status_code)
                response.close()
                return False
        except Exception as e:
            print(e)
            return False
    def switchBasedOnElevatorPosition(self, position):
        #type of position is tuple
        #print(type(position))
        print(type(position[1]))
        print(position[1])
        if position[1] == 0.:
            print("is 0")
            self.switchToDriverCam()
        elif position[1] == 3.:
            print("is 3")
            self.switchToVisionCam()
    def switchToVisionCam(self):
        print("switch to vision")
        # self.cap.release()
        # self.cap = cv2.VideoCapture(self.visionURL)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2)
        # self.url = self.visionURL
        self.vision = True
    def switchToDriverCam(self):
        print("switch to driver")
        # self.cap.release()
        # self.cap = cv2.VideoCapture(self.cam1URL)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2)
        # self.url = self.cam1URl
        self.vision = False
    def displayStream(self):
        ret, frame = self.cap.read()
        # if self.cnt > 60:
        #     self.cap.release()
        #     self.cap = cv2.VideoCapture(self.url)
        #     self.cnt = 0
        #     #print("cap resetted")
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
            self.timer.start()
            # self.startTime = time.time()
            self.cnt += 1
            return
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
            #self.startTime = time.time()
            self.cnt += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = CameraWidget()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec())
