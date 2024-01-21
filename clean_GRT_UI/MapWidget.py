import os
from PySide6.QtWidgets import QWidget, QLabel, QSizePolicy, QVBoxLayout
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt
import sys
from PySide6.QtWidgets import QApplication
    
class MapWidget(QWidget):
    def __init__(self, alliance, parent=None):
        super().__init__(parent)
        
        self.map_label = QLabel()
        self.map_label.setScaledContents(True)
        
        self.mapPixmap = QPixmap(f"{os.path.dirname(__file__)}/field24.png").scaled(600, 300) 
        self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/grt23robot.png")
        self.crosshairPixmap = QPixmap(f"{os.path.dirname(__file__)}/crosshair.png")
        
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
        
        # Set up QLabel for crosshair (position it at the center for now)
        self.crosshairLabel = QLabel(self)
        self.crosshairLabel.setGeometry(self.width() // 2 - self.crosshairPixmap.width() // 2,
                                        self.height() // 2 - self.crosshairPixmap.height() // 2,
                                        self.crosshairPixmap.width(), self.crosshairPixmap.height())
        self.crosshairLabel.setPixmap(self.crosshairPixmap)
        # self.crosshairLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.map_label.setPixmap(self.mapPixmap)
        layout = QVBoxLayout()
        layout.addWidget(self.map_label)
        self.setLayout(layout)
        
    def change_alliance_color(self, new_alliance_color):
        self.alliance = new_alliance_color
        self.reload_maps()

    def reload_maps(self):
        self.mapPixmap = QPixmap(f"{os.path.dirname(__file__)}/field24.png").scaled(600, 300)  
        rotation_angle = 90 if self.alliance == "red" else -90
        transform = QTransform().rotate(rotation_angle)
        self.mapPixmap = self.mapPixmap.transformed(transform)
        self.map_label.setPixmap(self.mapPixmap)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    mw = MapWidget('red')
    
    mw.show()
    sys.exit(app.exec())