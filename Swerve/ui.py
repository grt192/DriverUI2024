# -*- coding: utf-8 -*-
import sys
import time
from threading import Thread
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
from networktableHelper import networktableHelper

class MainWindow(QWidget):
    zoom1 = 0
    zoom2 = 0
    zoom3 = 0
    zoom4 = 0
    rotate1 = 0
    rotate2 = 0
    rotate3 = 0
    rotate4 = 0
    x1 = 495
    y1 = 260
    x2 = 905
    y2 = 260
    x3 = 495
    y3 = 640
    x4 = 905
    y4 = 640
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1920, 1080)
        self.setWindowTitle('Swerve')
        self.wheelPixmap = QPixmap("./RobotWheel.png")
        self.arrowPixmap = QPixmap("./arrow.png")
        # Get Position
        self.robot = QLabel(self)
        self.robot.setObjectName("robot")
        self.robotPixmap = QPixmap("./RobotFrame.png")
        self.robot.setPixmap(self.robotPixmap)
        self.robot.setGeometry(QtCore.QRect(450,200,500,500))
        self.networktableHelper = networktableHelper(self)
        t1 = Thread(target= self.refreshRobotLoop)
        #t1.start()

        self.robotWheel1 = QLabel(self)
        self.robotWheel1.setObjectName("robotWheel1")
        self.robotWheel1.setPixmap(QPixmap("./RobotWheel.png"))
        self.robotWheel1.setGeometry(455,220,80,80)

        self.arrow1 = QLabel(self)
        self.arrow1.setObjectName("arrow1")
        self.arrow1.setPixmap(QPixmap("./arrow.png"))
        self.arrow1.setGeometry(455,220,80,80)

        self.robotWheel2 = QLabel(self)
        self.robotWheel2.setObjectName("robotWheel2")
        self.robotWheel2.setPixmap(QPixmap("./RobotWheel.png"))
        self.robotWheel2.setGeometry(865,220,80,80)

        self.arrow2 = QLabel(self)
        self.arrow2.setObjectName("arrow2")
        self.arrow2.setPixmap(QPixmap("./arrow.png"))
        self.arrow2.setGeometry(865,220,80,80)

        self.robotWheel3 = QLabel(self)
        self.robotWheel3.setObjectName("robotWheel3")
        self.robotWheel3.setPixmap(QPixmap("./RobotWheel.png"))
        self.robotWheel3.setGeometry(455,600,80,80)

        self.arrow3 = QLabel(self)
        self.arrow3.setObjectName("arrow3")
        self.arrow3.setPixmap(QPixmap("./arrow.png"))
        self.arrow3.setGeometry(455,600,80,80)

        self.robotWheel4 = QLabel(self)
        self.robotWheel4.setObjectName("robotWheel4")
        self.robotWheel4.setPixmap(QPixmap("./RobotWheel.png"))
        self.robotWheel4.setGeometry(865,600,80,80)

        self.arrow4 = QLabel(self)
        self.arrow4.setObjectName("arrow4")
        self.arrow4.setPixmap(QPixmap("./arrow.png"))
        self.arrow4.setGeometry(865,600,80,80)


    def refreshRobotLoop(self):
        while True:
            time.sleep(0.02)
            self.refreshRobot()

    def refreshRobot(self):
        self.robotWheel1.setPixmap(self.wheelPixmap.transformed(QTransform.rotate(self.rotate1)))
        self.robotWheel2.setPixmap(self.wheelPixmap.transformed(QTransform.rotate(self.rotate2)))
        self.robotWheel3.setPixmap(self.wheelPixmap.transformed(QTransform.rotate(self.rotate3)))
        self.robotWheel4.setPixmap(self.wheelPixmap.transformed(QTransform.rotate(self.rotate4)))
        self.arrow1.setPixmap(self.arrowPixmap.transformed(QTransform.rotate(self.rotate1)))
        self.arrow2.setPixmap(self.arrowPixmap.transformed(QTransform.rotate(self.rotate2)))
        self.arrow3.setPixmap(self.arrowPixmap.transformed(QTransform.rotate(self.rotate3)))
        self.arrow4.setPixmap(self.arrowPixmap.transformed(QTransform.rotate(self.rotate4)))
        self.arrow1.move(self.x1 - self.zoom1 / 2, self.y1 - self.zoom1 / 2)
        self.arrow2.move(self.x2-self.zoom2/2,self.y2-self.zoom2/2)
        self.arrow3.move(self.x3-self.zoom3/2,self.y3-self.zoom3/2)
        self.arrow4.move(self.x4-self.zoom4/2,self.x4-self.zoom4/2)
    def r1(self, value):
        self.rotate1 = value
    def r2(self, value):
        self.rotate2 = value
    def r3(self, value):
        self.rotate3 = value
    def r4(self, value):
        self.rotate4 = value
    def v1(self, value):
        self.zoom1 = value
    def v2(self, value):
        self.zoom2 = value
    def v3(self, value):
        self.zoom3 = value
    def v4(self, value):
        self.zoom4 = value
if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())