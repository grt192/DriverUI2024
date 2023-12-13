# -*- coding: utf-8 -*-
import sys
import time
from threading import Thread
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from networktableHelper import networktableHelper

class getColorLabel(QLabel):
    def __init__(self, widget):
        super(getColorLabel, self).__init__(widget)
        self.main = widget

    def mousePressEvent(self, event):
        self.main.get(event.pos())


class MainWindow(QWidget):
    robotX = 0;
    robotY = 0;
    robotZ = 0;
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1920, 1080)
        self.setWindowTitle('Map Display Demo')

        # Get Position
        self.robot = QLabel(self)
        self.robot.setObjectName("robot")
        self.robotPixmap = QPixmap("./robotFrame.png")
        self.robot.setPixmap(self.robotPixmap)
        self.robot.setGeometry(QtCore.QRect(0,0,100,100))
        self.robot.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        print(">?")
        self.networktableHelper = networktableHelper(self)
        print("pa")
        t1 = Thread(target= self.refreshRobotLoop)
        print("??")
        t1.start()
    def get(self, pos):
        xIndex = pos.x()
        yIndex = pos.y()
        try:
            self.crosshair1.setGeometry(QtCore.QRect(xIndex-12.5,yIndex-12.5,25,25))
            self.crosshair1.show()
        except Exception as e:
            print(e)
        #self.crosshair1.lower()
        print(str(xIndex) + " "+ str(yIndex))
    def refreshRobotLoop(self):
        while True:
            time.sleep(0.02)
            self.refreshRobot()

    def refreshRobot(self):
        self.robot.hide()
        robotX = self.robotX
        robotY = self.robotY
        robotZ = self.robotZ
        if self.robotX<0 or self.robotY<0:
            return
        try:
            print(robotX)
            print(robotY)
            print(robotZ)
            self.robot.setPixmap(self.robotPixmap.transformed(QTransform.rotate(QTransform(),robotZ)))
            self.robot.move(int(robotX), int(robotY))
            self.robot.show()
        except Exception as e:
            print(e)
    def xChange(self, value):
        self.robotX = value
        #self.refreshRobot()
    def yChange(self, value):
        self.robotY = value
        #self.refreshRobot()
    def zChange(self, value):
        self.robotZ = value
        #self.refreshRobot()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())