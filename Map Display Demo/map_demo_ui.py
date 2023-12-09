# -*- coding: utf-8 -*-
import sys
import time
from threading import Thread
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from networktableHelper import networktableHelper

from pyqtgraph import ImageItem, ImageView
import numpy as np
import cv2
import os

class getColorLabel(QLabel):
    def __init__(self, widget):
        super(getColorLabel, self).__init__(widget)
        self.main = widget

    def mousePressEvent(self, event):
        self.main.get(event.pos())


class MainWindow(QMainWindow):
    robotX = 0
    robotY = 0
    robotZ = 0
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.resize(1920, 1080)
        self.setWindowTitle("GRT Driver Station - Map Demo")
        
        self.central_widget = QGraphicsView()
        self.setCentralWidget(self.central_widget)

        scene = QGraphicsScene(self)
        self.central_widget.setScene(scene)

        field_map = QGraphicsPixmapItem(QPixmap(f'{os.path.dirname(__file__)}/field23.png') )
        scene.addItem(field_map)

        robot_icon = QGraphicsPixmapItem(QPixmap(f'{os.path.dirname(__file__)}/grt23robot.png'))
        robot_icon.setPos(0, 0) 
        robot_icon.setScale(0.4) 
        scene.addItem(robot_icon)
        
        self.central_widget.fitInView(scene.sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        # self.crosshair1 = QLabel(self)
        # self.crosshair1.setObjectName("crosshair1")
        # self.crosshair1.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        # self.crosshair1.setPixmap(QPixmap('./crosshair.png'))
        # self.crosshair1.hide()

        # PREVIOUS ATTEMPT AT DOING THINGS: 
        
        # wid = QWidget(self)
        # self.setCentralWidget(wid)
        
        # self.map_layout = QVBoxLayout()
        
        # self.map_widget = ImageView()
        # map = cv2.imread(f'{os.path.dirname(__file__)}/field23.png') 
        # map = cv2.cvtColor(map, cv2.COLOR_BGR2RGB)
        # map = np.rot90(map)
        # self.map_widget.setImage(map)
        # self.map_layout.addWidget(self.map_widget)
        
        # wid.setLayout(self.map_layout)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())