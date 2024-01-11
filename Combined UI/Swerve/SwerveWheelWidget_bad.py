import os
from PyQt6.QtWidgets import QWidget, QLabel, QApplication
from PyQt6.QtGui import QPixmap, QTransform, QImageReader
from PySide6.QtCore import QTimer, QRect
# from PySide6.QtCore import 

from networktableHelper import networktableHelper  # You may need to adjust the import based on your project structure

class SwerveWheelWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1920, 1080)
        self.setWindowTitle('Swerve')

        self.wheelPixmap = QPixmap(f"{os.path.dirname(__file__)}/robot_wheel.png")
        self.arrowPixmap = QPixmap(f"{os.path.dirname(__file__)}/arrow.png")
        
        # self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/robot_frame.png")
        # self.robot.setPixmap(self.robotPixmap)
        # self.robot.setGeometry(QRect(450,200,500,500))

        self.create_wheel_and_arrow_widgets()

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_robot_loop)
        self.timer.start(1)

        self.networktableHelper = networktableHelper(self)

    def create_wheel_and_arrow_widgets(self):
        wheel_positions = [(450, 200), (865, 200), (450, 620), (865, 620)]

        self.robot = QLabel(self)
        self.robot.setScaledContents(True)
        self.robot.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/robot_frame.png"))
        self.robot.setGeometry(450, 200, 500, 500)

        self.robot_wheel_labels = []
        self.arrow_labels = []

        for i, (x, y) in enumerate(wheel_positions, start=1):
            wheel_label = QLabel(self)
            wheel_label.setObjectName(f"robotWheel{i}")
            wheel_label.setPixmap(self.wheelPixmap)
            wheel_label.setGeometry(x, y, 80, 80)

            arrow_label = QLabel(self)
            arrow_label.setObjectName(f"arrow{i}")
            arrow_label.setPixmap(self.arrowPixmap)
            arrow_label.setGeometry(x, y, 80, 80)

            self.robot_wheel_labels.append(wheel_label)
            self.arrow_labels.append(arrow_label)

    def refresh_robot_loop(self):
        self.refresh_robot()

    def refresh_robot(self):
        for i, (wheel_label, arrow_label) in enumerate(zip(self.robot_wheel_labels, self.arrow_labels), start=1):
            wheel_label.setPixmap(self.wheelPixmap.transformed(QTransform().rotate(getattr(self, f"module{i}rot"))))

        max_velocity = max(self.module1vel, self.module2vel, self.module3vel, self.module4vel)

        for arrow_label, velocity in zip(self.arrow_labels, [self.module1vel, self.module2vel, self.module3vel, self.module4vel]):
            scaled_size = 80 * velocity / max_velocity
            scaled_arrow = self.arrowPixmap.scaled(scaled_size, scaled_size)
            arrow_label.setPixmap(scaled_arrow.transformed(QTransform().rotate(getattr(self, f"module{i}rot"))))

            half_scaled_size = scaled_size / 2
            arrow_label.move(int(getattr(self, f"x{i}") - half_scaled_size), int(getattr(self, f"y{i}") - half_scaled_size))

    # Transform from radians to degrees
    def r1(self, value):
        setattr(self, "module1rot", value * 180 / 3.14)

    def r2(self, value):
        setattr(self, "module2rot", value * 180 / 3.14)

    def r3(self, value):
        setattr(self, "module3rot", value * 180 / 3.14)

    def r4(self, value):
        setattr(self, "module4rot", value * 180 / 3.14)

    # Add 1 to make sure size doesn't go below original size (at least zoomed x1)
    def v1(self, value):
        setattr(self, "module1vel", value + 1)

    def v2(self, value):
        setattr(self, "module2vel", value + 1)

    def v3(self, value):
        setattr(self, "module3vel", value + 1)

    def v4(self, value):
        setattr(self, "module4vel", value + 1)


if __name__ == '__main__':
    app = QApplication([])
    window = SwerveWheelWidget()
    window.show()
    app.exec()
