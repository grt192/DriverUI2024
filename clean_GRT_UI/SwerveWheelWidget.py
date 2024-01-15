# -*- coding: utf-8 -*-
import os
import sys
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6 import QtCore
from networktableHelper import networktableHelper

class SwerveWheelWidget(QWidget):
    module1vel = 0
    module2vel = 0
    module3vel = 0
    module4vel = 0
    module1rot = 0
    module2rot = 0
    module3rot = 0
    module4rot = 0
    #followings are positions for the 4 wheels.
    scale = 1
    x1 = 0# 450
    y1 = 0#200
    x2 = x1 + (415 * scale)
    y2 = y1
    x3 = x1
    y3 = y1 + (420 * scale)
    x4 = x2
    y4 = y3
    
    
    def __init__(self):
        super(SwerveWheelWidget, self).__init__()
        
        self.wheelPixmap = QPixmap(f"{os.path.dirname(__file__)}/robot_wheel.png")
        self.arrowPixmap = QPixmap(f"{os.path.dirname(__file__)}/arrow.png")
        
        # Get Position
        self.robot = QLabel(self)
        self.robot.setObjectName("robot")
        self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/robot_frame.png")
        self.robot.setPixmap(self.robotPixmap)
        self.robot.setGeometry(QtCore.QRect(self.x1 * self.scale,self.y2 * self.scale, 500 * self.scale, 500 * self.scale))
        self.networktableHelper = networktableHelper(self)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refreshRobotLoop)
        self.timer.start(1)
        
        self.robotWheel1 = QLabel(self)
        self.robotWheel2 = QLabel(self)
        self.robotWheel3 = QLabel(self)
        self.robotWheel4 = QLabel(self)
        self.arrow1 = QLabel(self)
        self.arrow2 = QLabel(self)
        self.arrow3 = QLabel(self)
        self.arrow4 = QLabel(self)
        
        self.determine_geometries()
        
    def determine_geometries(self):
        
        self.robotWheel1.setObjectName("robotWheel1")
        self.robotWheel1.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/robot_wheel.png"))
        self.robotWheel1.setGeometry(self.x1 * self.scale, self.y1 * self.scale,80 * self.scale,80 * self.scale)

        self.arrow1.setObjectName("arrow1")
        self.arrow1.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/arrow.png"))
        self.arrow1.setGeometry(self.x1 * self.scale, self.y1 * self.scale,80 * self.scale,80 * self.scale)

        self.robotWheel2.setObjectName("robotWheel2")
        self.robotWheel2.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/robot_wheel.png"))
        self.robotWheel2.setGeometry(self.x2 * self.scale, self.y2 * self.scale,80 * self.scale,80 * self.scale)

        self.arrow2.setObjectName("arrow2")
        self.arrow2.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/arrow.png"))
        self.arrow2.setGeometry(self.x2 * self.scale, self.y2 * self.scale, 80 * self.scale, 80 * self.scale)

        self.robotWheel3.setObjectName("robotWheel3")
        self.robotWheel3.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/robot_wheel.png"))
        self.robotWheel3.setGeometry(self.x3 * self.scale, self.y3 * self.scale, 80 * self.scale, 80 * self.scale)

        self.arrow3.setObjectName("arrow3")
        self.arrow3.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/arrow.png"))
        self.arrow3.setGeometry(self.x3 * self.scale, self.y3 * self.scale, 80 * self.scale, 80 * self.scale)

        self.robotWheel4.setObjectName("robotWheel4")
        self.robotWheel4.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/robot_wheel.png"))
        self.robotWheel4.setGeometry(self.x4 * self.scale, self.y4 * self.scale, 80 * self.scale, 80 * self.scale)

        self.arrow4.setObjectName("arrow4")
        self.arrow4.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/arrow.png"))
        self.arrow4.setGeometry(self.x4 * self.scale, self.y4 * self.scale, 80 * self.scale, 80 * self.scale)

    def resizeEvent(self, resize):
        xSize, ySize = resize.size().toTuple()
        self.scale = min(xSize/500, ySize/500)
        # print(self.scale)
        self.determine_geometries()
    
    def refreshRobotLoop(self):

        # print(self.size())
        self.refreshRobot()
        self.timer.start(1)
        
        self.widget_size = self.size()

    def refreshRobot(self):
        
        self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/robot_frame.png").scaled(500 * self.scale, 500 * self.scale, aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.robot.setPixmap(self.robotPixmap)
        self.robot.setGeometry(QtCore.QRect(self.x1 * self.scale,self.y2 * self.scale, 500 * self.scale, 500 * self.scale))
        # self.robot.setGeometry(QtCore.QRect(self.x1,self.y2))
        
        #might get errors because of floats. Change floats to int may help address potential errors.
        self.robotWheel1.setPixmap(self.wheelPixmap.scaled(80 * self.scale, 80 * self.scale, aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self.module1rot)))
        self.robotWheel2.setPixmap(self.wheelPixmap.scaled(80 * self.scale, 80 * self.scale, aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self.module2rot)))
        self.robotWheel3.setPixmap(self.wheelPixmap.scaled(80 * self.scale, 80 * self.scale, aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self.module3rot)))
        self.robotWheel4.setPixmap(self.wheelPixmap.scaled(80 * self.scale, 80 * self.scale, aspectMode=QtCore.Qt.AspectRatioMode.KeepAspectRatio).transformed(QTransform().rotate(self.module4rot)))
        
        scaledSize1 = 80*self.module1vel * self.scale
        scaledSize2 = 80*self.module2vel * self.scale
        scaledSize3 = 80*self.module3vel * self.scale
        scaledSize4 = 80*self.module4vel * self.scale
        
        scaledArrow1 = self.arrowPixmap.scaled(scaledSize1, scaledSize1)
        scaledArrow2 = self.arrowPixmap.scaled(scaledSize2, scaledSize2)
        scaledArrow3 = self.arrowPixmap.scaled(scaledSize3, scaledSize3)
        scaledArrow4 = self.arrowPixmap.scaled(scaledSize4, scaledSize4)
        self.arrow1.setPixmap(scaledArrow4.transformed(QTransform().rotate(self.module1rot)))
        self.arrow2.setPixmap(scaledArrow4.transformed(QTransform().rotate(self.module2rot)))
        self.arrow3.setPixmap(scaledArrow4.transformed(QTransform().rotate(self.module3rot)))
        self.arrow4.setPixmap(scaledArrow4.transformed(QTransform().rotate(self.module4rot)))
        halfScaledSize1 = scaledSize1/2
        halfScaledSize2 = scaledSize2/2
        halfScaledSize3 = scaledSize3/2
        halfScaledSize4 = scaledSize4/2
        self.arrow1.move(int(self.x1 * self.scale - halfScaledSize1), int(self.y1 - halfScaledSize1))
        self.arrow2.move(int(self.x2 - halfScaledSize2), int(self.y2 - halfScaledSize2))
        self.arrow3.move(int(self.x3 - halfScaledSize3), int(self.y3 - halfScaledSize3))
        self.arrow4.move(int(self.x4 - halfScaledSize4), int(self.y4 - halfScaledSize4))
    #Tranform from radians to degrees
    def r1(self, value):
        self.module1rot = value*180/3.14
    def r2(self, value):
        self.module2rot = value*180/3.14
    def r3(self, value):
        self.module3rot = value*180/3.14
    def r4(self, value):
        self.module4rot = value*180/3.14
    #add 1 to make sure size doesn't go below original size (at least zoomed x1)
    def v1(self, value):
        self.module1vel = value+1
    def v2(self, value):
        self.module2vel = value+1
    def v3(self, value):
        self.module3vel = value+1
    def v4(self, value):
        self.module4vel = value+1
if __name__ == '__main__':
    app = QApplication([])
    window = SwerveWheelWidget()
    window.show()
    sys.exit(app.exec())