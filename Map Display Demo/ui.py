# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PIL import ImageQt

class getColorLabel(QLabel):
    def __init__(self, widget):
        super(getColorLabel, self).__init__(widget)
        self.main = widget

    def mousePressEvent(self, event):
        self.main.get(event.pos())


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(1920, 1080)
        self.setWindowTitle('Map Display Demo')

        # Get Position
        self.label = getColorLabel(self)
        self.label.setGeometry(0, 0, 780, 400)
        self.label.setPixmap(QPixmap('./AnimeGirl.png'))
        self.label.setScaledContents(True)

        self.crosshair1 = QLabel(self)
        self.crosshair1.setObjectName("crosshair1")
        self.crosshair1.setPixmap(QPixmap('./crosshair.png'))
        self.crosshair1.hide()
    def get(self, pos):
        xIndex = pos.x()
        yIndex = pos.y()
        self.crosshair1.setGeometry(QtCore.QRect(xIndex-100,yIndex-100,500,500))
        self.crosshair1.show()
        print(str(xIndex) + " "+ str(yIndex))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())