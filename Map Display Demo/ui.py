# -*- coding: utf-8 -*-
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6 import QtCore
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
        self.crosshair1.setGeometry(QtCore.QRect(xIndex-12.5,yIndex-12.5,25,25))
        self.crosshair1.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.crosshair1.show()
        #self.crosshair1.lower()
        print(str(xIndex) + " "+ str(yIndex))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())