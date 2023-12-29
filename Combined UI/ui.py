from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from networktableHelper import networktableHelper
from mapLabel import mapLabel


class MyWindow(QMainWindow):
    QCheckBoxWidth = 50
    QCheckBoxHeight = 50
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Tabbed Window Example")
        self.resize(1920, 1080)
        # Create the tab widget
        self.tab_widget = QTabWidget(self)

        # Create and add tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tab_widget.addTab(self.tab1, "Tab 1")
        self.tab_widget.addTab(self.tab2, "Tab 2")

        # Add content to Tab 1
        # crosshair.png is 30*30
        self.crosshair1 = QLabel(self.tab1)
        self.crosshair1.setObjectName("crosshair1")
        self.crosshair1.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.crosshair1.setPixmap(QPixmap("./crosshair.png"))
        self.crosshair1.hide()

        self.robot = QLabel(self.tab1)
        self.robot.setObjectName("robot")
        self.robotPixmap = QPixmap("./RobotArrow.png")
        self.robot.setPixmap(self.robotPixmap)
        self.robot.setGeometry(QtCore.QRect(15, 15, 30, 30))
        self.robot.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.robot.hide()

        self.field = mapLabel(self.tab1, self)
        self.field.setObjectName("field")
        self.fieldPixmap = QPixmap("./field23.png").scaled(600, 300)
        self.field.setPixmap(self.fieldPixmap)
        self.fieldOffsetX = 20
        self.fieldOffsetY = 740
        self.field.setGeometry(QtCore.QRect(self.fieldOffsetX, self.fieldOffsetY, 600, 300))

        self.clickXDisplay = QLabel(self.tab1)
        self.clickXDisplay.setGeometry(1880, 50, 20, 10)

        self.clickYDisplay = QLabel(self.tab1)
        self.clickYDisplay.setGeometry(1880, 65, 20, 10)

        self.visionSwitch = QCheckBox(self.tab1)
        self.visionSwitch.setGeometry(QRect(1850, 80, self.QCheckBoxWidth, self.QCheckBoxHeight))

        tab1StyleSheetFile = QFile("./tab1StyleSheet.qss")
        tab1StyleSheetFile.open(QFile.OpenModeFlag.ReadOnly)
        try:
            tab1StyleSheet = tab1StyleSheetFile.readAll().toStdString()
            self.tab1.setStyleSheet(tab1StyleSheet)
            #print(str(tab1StyleSheet))
            #self.setStyleSheet("QCheckBox::indicator {width: 50;height: 59px;}")
        except Exception as e:
            print(e)

        # Set the central widget to the tab widget
        self.setCentralWidget(self.tab_widget)
        self.networktableHelper = networktableHelper(self)



    def getClickPosition(self, pos):
        print(str(pos.x()) + " " + str(pos.y()))
        self.clickXDisplay.setText(str(pos.x()))
        self.clickYDisplay.setText(str(pos.y()))
        self.crosshair1.setGeometry(pos.x() - 9 + self.fieldOffsetX, pos.y() - 9 + self.fieldOffsetY, 20, 20)
        self.crosshair1.show()
        self.crosshair1.raise_()


def main():
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
