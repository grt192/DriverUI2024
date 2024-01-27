from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import *
import sys
from PySide6.QtWidgets import QApplication
    
class MapDisplayWidget(QWidget):
    newCrosshairPosition = Signal(tuple)
    def __init__(self, alliance, parent=None):
        super().__init__(parent)
        
        self.mapLabel = QLabel()
        self.mapLabel.setScaledContents(True)
        
        self.mapPixmap = QPixmap("./Images/field24.png").scaled(600, 300)
        self.robotPixmap = QPixmap("./Images/grt23robot.png")
        self.crosshairPixmap = QPixmap("./Images/crosshair.png")
        
        self.alliance = alliance

        if self.alliance == "red":
            rotationAngle = 90
        else:
            rotationAngle = -90
        transform = QTransform().rotate(rotationAngle)
        self.mapPixmap = self.mapPixmap.transformed(transform)
        
        # Set up QLabel for robot icon
        self.robotLabel = QLabel(self)
        self.robotLabel.setPixmap(self.robotPixmap)
        self.robotLabel.setMask(self.robotPixmap.mask())  # Use transparency information for masking
        
        # Set up QLabel for crosshair (hide it for now)
        self.crosshairLabel = QLabel(self)
        self.crosshairLabel.setPixmap(self.crosshairPixmap)
        self.crosshairLabel.hide()
        self.crosshairLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)\

        #init crosshair position
        self.crosshairX = None
        self.crosshairY = None
        # Set up layout
        
        self.mapLabel.setPixmap(self.mapPixmap)
        layout = QVBoxLayout()
        layout.addWidget(self.mapLabel)
        self.setLayout(layout)
        
    def changeAllianceColor(self, new_alliance_color):
        self.alliance = new_alliance_color
        self.reloadMaps()

    def reloadMaps(self):
        self.mapPixmap = QPixmap("./Images/field24.png").scaled(600, 300)
        rotation_angle = 90 if self.alliance == "red" else -90
        transform = QTransform().rotate(rotation_angle)
        self.mapPixmap = self.mapPixmap.transformed(transform)
        self.mapLabel.setPixmap(self.mapPixmap)

    def mousePressEvent(self, event):
        # Get the position of the mouse click
        position = event.pos()
        print(f"Clicked at position: {position.x()}, {position.y()}")
        self.crosshairLabel.hide()
        self.crosshairLabel.setGeometry(position.x() - 12, position.y() - 12, 25, 25)
        self.crosshairX = position.x()
        self.crosshairY = position.y()
        self.crosshairLabel.show()

        self.newCrosshairPosition.emit((self.crosshairX, self.crosshairY))

        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MapDisplayWidget('red')
    
    mw.show()
    sys.exit(app.exec())