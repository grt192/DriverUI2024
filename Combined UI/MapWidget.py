import os
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap, QTransform

class GRTMapWidget(QWidget):
    def __init__(self, alliance, parent=None):
        super().__init__(parent)

        # Load map field, robot image, and crosshair image
        self.mapPixmap = QPixmap(f"{os.path.dirname(__file__)}/field24.png").scaled(600, 300)  # Adjust the path accordingly
        self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/grt23robot.png")
        self.crosshairPixmap = QPixmap(f"{os.path.dirname(__file__)}/crosshair.png")
        self.alliance = alliance

        # Set up QLabel for map field
        rotation_angle = 90 if self.alliance == "red" else -90
        transform = QTransform().rotate(rotation_angle)
        self.mapPixmap = self.mapPixmap.transformed(transform)
        
        self.mapLabel = QLabel(self)
        self.mapLabel.setGeometry(0, 0, self.mapPixmap.width(), self.mapPixmap.height())
        self.mapLabel.setPixmap(self.mapPixmap)

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
        
        # Set up initial rotation based on self.alliance
        self.rotate_map()

    def rotate_map(self):
        # Rotate map field based on self.alliance
        rotation_angle = 90 if self.alliance == "red" else -90
        transform = QTransform().rotate(rotation_angle)
        # self.mapPixmap = self.mapPixmap.transformed(transform)
        # self.mapLabel.setPixmap(self.mapPixmap)

        # Rotate robot icon based on self.alliance
        self.robotPixmap = self.robotPixmap.transformed(transform)
        self.robotLabel.setPixmap(self.robotPixmap)

    def set_alliance(self, alliance):
        self.alliance = alliance
        self.rotate_map()

    def set_robot_position(self, x, y):
        # Set the position of the robot icon on the map
        self.robotLabel.setGeometry(x, y, self.robotPixmap.width(), self.robotPixmap.height())

    def set_crosshair_position(self, x, y):
        # Set the position of the crosshair on the map
        self.crosshairLabel.setGeometry(x, y, self.crosshairPixmap.width(), self.crosshairPixmap.height())

# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication

#     class MainApp(QApplication):
#         def __init__(self, argv):
#             super(MainApp, self).__init__(argv)
#             self.main_window = GRTMapWidget()
#             self.main_window.show()

#     app = MainApp(sys.argv)
#     sys.exit(app.exec())