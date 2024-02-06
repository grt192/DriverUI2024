import sys
import time
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import numpy as np
from time import perf_counter
import cv2
import requests
from threading import *


class CameraWidget(QWidget):
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
            print(self.url)
            self.response = requests.get(self.url, stream=True)
            self.bytes = b''
        else:
            self.url = None

        self.cap = cv2.VideoCapture(self.url)
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
        layout.addWidget(self.errorLabel)
        layout.addWidget(self.reconnectButton)


    def reconnect(self):
        self.cap = cv2.VideoCapture(self.url)
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

    def update_frame(self):
        # FETCH IMAGE DATA
        image_data = np.random.random((160, 320)) * 255  # Example random image data
        height, width = image_data.shape

        # Convert NumPy array to QImage
        image = QImage(image_data.data, width, height, width, QImage.Format.Format_Grayscale8)

        # Convert QImage to QPixmap and set it to the QLabel
        pixmap = QPixmap.fromImage(image)
        self.cameraDisplay.setPixmap(pixmap.scaled(pixmap.size(), aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        self.time_now = time.time()
        self.actual_fps = 1 / self.calculate_actual_fps(self.time_now - self.time_old)
        self.time_old = self.time_now

        #Start timer for next frame.
        self.timer.start(1)
        now = perf_counter()
        elapsed_now = now - self.updateTime
        self.updateTime = now
        self.elapsed = self.elapsed * 0.9 + elapsed_now * 0.1
        self.errorLabel.setText(str(round(self.actual_fps, 2)) + " FPS")

    def calculate_actual_fps(self, latest_instantaneous_fps):
        self.past_five_instantaneous_fps.pop(0)
        self.past_five_instantaneous_fps.append(latest_instantaneous_fps)

        total = sum(self.past_five_instantaneous_fps)
        avg = total / 5
        return avg


    def displayStream(self):
        ret, frame = self.cap.read()
        if self.cnt > 60:
            self.cap.release()
            self.cap = cv2.VideoCapture(self.url)
            self.cnt = 0
            print("cap resetted")
        if ret:
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


class DriverCameraWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DriverCameraWindow, self).__init__(parent)
        self.setWindowTitle("GRT Driver Camera")

        wid = QWidget(self)  # Define Window Widget
        self.setCentralWidget(wid)

        self.camera_widget = CameraWidget(self)

        layout = QVBoxLayout()
        layout.addWidget(self.camera_widget)

        wid.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = DriverCameraWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec())
