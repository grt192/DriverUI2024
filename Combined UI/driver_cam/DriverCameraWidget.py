import sys
import time
from threading import Thread
from PySide6 import QtCore
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from pyqtgraph import ImageItem, PlotWidget
import numpy as np
from time import perf_counter

class CameraWidget(QWidget):
    def __init__(self, parent=None):
        super(CameraWidget, self).__init__(parent)

        # self.plot = PlotWidget()
        
        self.camera_display = QLabel()
        image_data = np.random.random((160, 320)) * 255  # Example random image data
        height, width = image_data.shape

        # Convert NumPy array to QImage
        image = QImage(image_data.data, width, height, width, QImage.Format.Format_Grayscale8)
        
        # Convert QImage to QPixmap and set it to the QLabel
        pixmap = QPixmap.fromImage(image)
        self.camera_display.setPixmap(pixmap)

        # self.plot.addItem(self.camera_display)
        # self.plot.hideAxis('left')
        # self.plot.hideAxis('bottom')
        # self.plot.setMouseEnabled()

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)

        self.actual_fps = 0
        self.past_five_instantaneous_fps = [0, 0, 0, 0, 0]
        self.updateTime = perf_counter()
        self.elapsed = 0
        self.time_old = time.time()

        layout = QVBoxLayout(self)
        layout.addWidget(self.camera_display)
        layout.addWidget(self.errorLabel)

    def update_frame(self):
        # FETCH IMAGE DATA
        image_data = np.random.random((160, 320)) * 255  # Example random image data
        height, width = image_data.shape

        # Convert NumPy array to QImage
        image = QImage(image_data.data, width, height, width, QImage.Format.Format_Grayscale8)
        
        # Convert QImage to QPixmap and set it to the QLabel
        pixmap = QPixmap.fromImage(image)
        self.camera_display.setPixmap(pixmap)

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


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     player = DriverCameraWindow()
#     player.resize(640, 480)
#     player.show()
#     sys.exit(app.exec())
