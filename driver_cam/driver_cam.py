import os
import sys
import time
from threading import Thread
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from networktableHelper import networktableHelper

from pyqtgraph import ImageView
import numpy as np
from time import perf_counter

class DriverCameraWidget(QMainWindow):
    
    def __init__(self, parent=None):
        super(DriverCameraWidget, self).__init__(parent)
        self.setWindowTitle("GRT Driver Camera")
        
        wid = QWidget(self) # Define Window Widget
        self.setCentralWidget(wid)
        
        self.camera_display = ImageView()
        self.camera_display.setImage(np.random.random((320,160)))
        
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)
        
        self.actual_fps = 0

        self.past_five_instantaneous_fps = [0,0,0,0,0]
        
        self.updateTime = perf_counter()
        
        self.elapsed = 0
        self.time_old = time.time()
        
        layout = QVBoxLayout()
        layout.addWidget(self.camera_display)
        layout.addWidget(self.errorLabel)
        
        wid.setLayout(layout)
        
    def update_frame(self):
        #FETCH IMAGE DATA
        self.camera_display.setImage(np.random.random((320,160)))
        
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
        avg = total/5
        return avg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = DriverCameraWidget()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec())