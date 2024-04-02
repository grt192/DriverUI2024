import sys
from PySide6 import QtCore
from PySide6.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGroupBox
from PySide6.QtWidgets import QApplication, QSizePolicy
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import Qt
import cv2
import requests


class CameraWidget(QWidget):
    camURl = "http://10.1.92.2:1181/stream.mjpg"
    camTestURL = "http://10.1.92.2:1181"
    #320*240@120fps for fisheye
    resolutionX = 160
    resolutionY = 120
    
    FPS = 30
    # resolutionX = 320
    # resolutionY = 240

    scale = 4
    #The actual video size on the UI
    windowWidth = resolutionX * scale
    windowHeight = resolutionY * scale

    connected = False
    def __init__(self, parent=None):
        super(CameraWidget, self).__init__(parent)

        self.cameraDisplay = QLabel(self)
        self.cameraDisplay.setScaledContents(True)
        self.cameraDisplay.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cameraDisplay.setMaximumWidth(self.windowWidth)
        self.cameraDisplay.setMaximumHeight(self.windowHeight)

        #use this time to call the DisplayStream method to retrieve and display frames.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.displayStream)
        # self.timer.timeout.connect(self.testDisplay)
        self.timer.setSingleShot(True)
        self.timer.start(1)

        if self.checkDriverCam():
            self.setDriverCapture()
            self.connected = True
        
        self.reconnectButton = QPushButton("Reconnect to Driver Cams")
        self.reconnectButton.clicked.connect(self.reconnect)

        layout = QVBoxLayout(self)

        #Add everything layout.
        layout.addWidget(self.cameraDisplay, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.reconnectButton)
        
        main_layout = QVBoxLayout()
        self.group_box = QGroupBox("Driver Camera")
        self.group_box.setLayout(layout)
        main_layout.addWidget(self.group_box)
        
        self.setLayout(main_layout)


    def setDriverCapture(self):
        self.driverCapture = cv2.VideoCapture(self.camURl)
        self.driverCapture.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolutionX)
        self.driverCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolutionY)
        self.driverCapture.set(cv2.CAP_PROP_FPS, self.FPS)
        # self.driverCap.set(cv2.CAP_PROP_EXPOSURE, 0.5)
        # self.driverCap.set(cv2.CAP_PROP_CONVERT_RGB, 1)
    def reconnect(self):
        self.connected = self.checkDriverCam()
        if self.connected:
            self.setDriverCapture()
            self.timer.start(1)
        else:
            print("[DriverCameraWidget] Network Issue! Unable to connect.")
    
    def checkDriverCam(self):
        try:
            response = requests.get(self.camTestURL, timeout=1)
            if response.status_code != 200:
                print("[DriverCameraWidget] Driver cam not accessible! Status Code: " + str(response.status_code))
                return False
            response.close()
        except Exception as e:
            print("[DriverCameraWidget] Check Driver exception in the following line:")
            print(e)
            return False
        return True
    
    def testDisplay(self):
        ret, frame = self.driverCapture.read()
        cv2.imshow("frame", frame)
        cv2.waitKey(1)
        self.timer.start(1)

    def displayStream(self):
        if not self.connected:
            pixmap = QPixmap(self.resolutionX * self.scale, self.resolutionY * self.scale)  # Adjust size as needed
            pixmap.fill(Qt.black)  # Fill with black color
            
            self.cameraDisplay.setPixmap(pixmap)
            self.cameraDisplay.setAlignment(Qt.AlignCenter)
            self.timer.start(1)
            return
        elif not self.driverCapture.isOpened():
            print("[DriverCameraWidget] Can't access driver camera")
            return
        else:
            ret, frame = self.driverCapture.read()
            # Convert the image to Qt format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            cvtToQtFormat = QImage(
                frame.data, w, h, bytesPerLine, QImage.Format_RGB888
            )
            pixmap = QPixmap.fromImage(cvtToQtFormat)
            self.cameraDisplay.setPixmap(pixmap)
            self.cameraDisplay.setAlignment(Qt.AlignCenter)
            self.timer.start(1)