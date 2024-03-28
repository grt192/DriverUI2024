from Widgets.ToggleWidget import ToggleWidget
from PySide6.QtWidgets import QWidget, QHBoxLayout
from Helpers.NetworktableHelper import NetworkTableManager
class PoseSwitchWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.enableVision= ToggleWidget(
            "Vision", "Vision", "visionEnabled",
            ("Vision Enabled", "Vision Disabled"), ("green", "red")
        )
        self.enableOdometry = ToggleWidget(
            "Odometry", "Odometry", "odometryEnabled",
            ("Odometry Enabled", "Odometry Disabled"), ("green", "red")
        )

        layout = QHBoxLayout(self)
        layout.addWidget(self.enableVision)
        layout.addWidget(self.enableOdometry)