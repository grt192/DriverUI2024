# -*- coding: utf-8 -*-
import os
import sys
import time
from threading import Thread
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6 import QtCore
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

        self.crosshair1 = QLabel(self)
        self.crosshair1.setObjectName("crosshair1")
        self.crosshair1.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        # self.crosshair1.setPixmap(QPixmap('./crosshair.png'))
        self.crosshair1.setPixmap(QPixmap(f'{os.path.dirname(__file__)}/crosshair.png'))
        
        self.crosshair1.hide()

        self.robot = QLabel(self)
        self.robot.setObjectName("robot")
        # self.robotPixmap = QPixmap("./RobotArrow.png")
        self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/RobotArrow.png")
        
        self.robot.setPixmap(self.robotPixmap)
        self.robot.setGeometry(QtCore.QRect(15,15,30,30))
        self.robot.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        #print(">?")
        self.networktableHelper = networktableHelper(self)
        #print("pa")
        t1 = Thread(target= self.refreshRobotLoop)
        #print("??")
        t1.start()

        self.field = QLabel(self)
        self.field.setObjectName("field")
        try:
            # self.fieldPixmap = QPixmap("./field23.png").scaled(1200,600)
            self.fieldPixmap = QPixmap(f"{os.path.dirname(__file__)}/field23.png").scaled(1200,600)
            
            self.field.setPixmap(self.fieldPixmap)
            self.field.setGeometry(QtCore.QRect(100,100,1200,600))
        except Exception as e:
            print(e)
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
            print("x: "+str(robotX))
            print("y: "+str(robotY))
            print("z: "+str(robotZ))
            self.robot.setPixmap(self.robotPixmap.transformed(QTransform.rotate(QTransform(),robotZ-90)))
            #if(robotZ<0)
            self.robot.move(int(robotX/651.25*1200-15)+100, int(700-(robotY/315.5*600))-15)
            self.robot.show()
        except Exception as e:
            print(e)
        self.robot.raise_()
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