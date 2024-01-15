import sys
import time
from threading import Thread
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from pyqtgraph import ImageItem, PlotWidget
import numpy as np
from time import perf_counter
import cv2
import requests
from threading import *


class CameraWidget(QWidget):
    def __init__(self, displayName='GRT Driver Cam', parent=None):
        super(CameraWidget, self).__init__(parent)

        # self.plot = PlotWidget()

        self.display_name = QLabel(displayName)
        self.display_name.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        self.camera_display = QLabel()
        self.camera_display.setScaledContents(True)
        self.camera_display.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Check if network is available
        self.is_network_available = self.check_network()

        # self.plot.addItem(self.camera_display)
        # self.plot.hideAxis('left')
        # self.plot.hideAxis('bottom')
        # self.plot.setMouseEnabled()

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        if self.is_network_available:
            # Fetch video stream from the network
            self.url = "http://10.1.92.2:1181/stream.mjpg"
            self.response = requests.get(self.url, stream=True)
            self.bytes = b''
        else:
            # Display random image data
            image_data = np.random.random((160, 320)) * 255  # Example random image data
            height, width = image_data.shape

            # Convert NumPy array to QImage
            image = QImage(image_data.data, width, height, width, QImage.Format.Format_Grayscale8)

            # Convert QImage to QPixmap and set it to the QLabel
            pixmap = QPixmap.fromImage(image)
            self.camera_display.setPixmap(pixmap.scaled(pixmap.size(), aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.DisplayStream)
        self.timer.start(1)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)

        self.CamThread = Thread(target=self.DisplayStream)
        self.CamThread.start()

        self.actual_fps = 0
        self.past_five_instantaneous_fps = [0, 0, 0, 0, 0]
        self.updateTime = perf_counter()
        self.elapsed = 0
        self.time_old = time.time()

        layout = QVBoxLayout(self)
        
        layout.addWidget(self.display_name)
        layout.addWidget(self.camera_display)
        layout.addWidget(self.errorLabel)


    def check_network(self):
        # Check if network is available
        try:
            response = requests.get("http://10.1.92.2:1181", timeout=2)
            return True
        except requests.ConnectionError:
            return False

    def update_frame(self):
        # FETCH IMAGE DATA
        if not self.is_network_available:
            image_data = np.random.random((160, 320)) * 255  # Example random image data
            height, width = image_data.shape

            # Convert NumPy array to QImage
            image = QImage(image_data.data, width, height, width, QImage.Format.Format_Grayscale8)

            # Convert QImage to QPixmap and set it to the QLabel
            pixmap = QPixmap.fromImage(image)
            self.camera_display.setPixmap(pixmap.scaled(pixmap.size(), aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))

            self.time_now = time.time()
            self.actual_fps = 1 / self.calculate_actual_fps(self.time_now - self.time_old)
            self.time_old = self.time_now

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

    def DisplayStream(self):
        try:
            if self.is_network_available:
                for chunk in self.response.iter_content(chunk_size=1024):
                    self.bytes += chunk
                    a = self.bytes.find(b'\xff\xd8')  # JPEG start
                    b = self.bytes.find(b'\xff\xd9')  # JPEG end
                    if a != -1 and b != -1:
                        jpg = self.bytes[a:b + 2]  # Extract the JPEG image
                        bytes = self.bytes[b + 2:]  # Remove the processed bytes

                        # Decode the JPEG image to a frame
                        try:
                            frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        except Exception as e:
                            print(e)

                        # Convert to QImage
                        height, width, channel = frame.shape
                        bytesPerLine = 3 * width
                        qImg = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
                        pixmap = QPixmap.fromImage(qImg)
                        scaledPixmap = pixmap.scaled(300, 300)

                        self.camera_display.setPixmap(scaledPixmap.scaled(scaledPixmap.size(), aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio))
                        self.response.close()
                        self.response = requests.get(url=self.url, stream=True)
                        self.bytes = b''
                        return
            else:
                self.update_frame()
        except Exception as e:
            # self.response = requests.get(self.url, stream=True)
            # self.bytes = b''
            print(e)


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
