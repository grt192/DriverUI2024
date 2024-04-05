from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QLabel
from Widgets.CustomWidgets.BaseWidgets.GradientWarningDoubleDisplayLabel import GradientWarningDoubleDisplayLabel

class MotorWidget(QWidget):
    def __init__(self, NTName: str, name: str, timer: QTimer, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.name = name
        self.timer = timer
        self.nameLabel = QLabel(name)
        self.nameLabel.setStyleSheet("color: red; background-color: black; font-size: 14px")
        self.currentLabel = GradientWarningDoubleDisplayLabel(
            "C", "Motors", NTName + "Current",
            (153, 215, 189), (243, 95, 0),
            0, 40,
            self.timer,
            "color: white; font-weight: bold; font-size: 12px;",
            parent=self, debug=False
        )
        self.temperatureLabel = GradientWarningDoubleDisplayLabel(
            "T", "Motors", NTName + "Temperature",
            (153, 215, 189), (243, 95, 0),
            10, 50,
            self.timer,
            "color: white; font-weight: bold; font-size: 12px;",
            parent=self, debug=False
        )
        self.voltageLabel = GradientWarningDoubleDisplayLabel(
            "V", "Motors", NTName + "Voltage",
            (0, 180, 70), (1, 181, 71),
            12, 13,
            self.timer,
            "color: white; font-weight: bold; font-size: 12px;",
            parent=self, debug=False
        )

        layout = QHBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.currentLabel)
        layout.addWidget(self.temperatureLabel)
        layout.addWidget(self.voltageLabel)


    def updateLabels(self):
        self.currentLabel.manualUpdate()
        self.voltageLabel.manualUpdate()
        self.temperatureLabel.manualUpdate()