from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QPushButton
from Widgets.CustomWidgets.BaseWidgets.BoolDisplayLabel import BoolDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.ConnectionDisplayLabel import ConnectionDisplayLabel
from Widgets.CustomWidgets.AllianceLabel import AllianceLabel
from Widgets.CustomWidgets.BaseWidgets.GradientDoubleDisplayLabel import GradientDoubleDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.GradientWarningDoubleDisplayLabel import GradientWarningDoubleDisplayLabel

class InfoWidget2(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.timer = QTimer()
        self.timer.start(500)
        self.motor10CurrentLabel = GradientWarningDoubleDisplayLabel(
            "10 Current", "Motors", "10Current",
            (0, 180, 70), (1, 181, 71),
            0, 40,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent=self, debug=False
        )
        self.motor10VoltageLabel = GradientWarningDoubleDisplayLabel(
            "10 Voltage: ", "Motors", "10Voltage",
            (0, 180, 70), (1, 181, 71),
            12, 13,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent=self, debug=False
        )

        self.motor10TemperatureLabel = GradientWarningDoubleDisplayLabel(
            "10 Temp", "Motors", "10Temperature",
            (153, 215, 189), (243, 95, 0),
            10, 50,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent=self, debug=False
        )
        self.motor11CurrentLabel = GradientWarningDoubleDisplayLabel(
            "11 Current", "Motors", "11Current",
            (0, 180, 70), (1, 181, 71),
            0, 40,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent=self, debug=False
        )
        self.motor11VoltageLabel = GradientWarningDoubleDisplayLabel(
            "11 Voltage: ", "Motors", "11Voltage",
            (0, 180, 70), (1, 181, 71),
            12, 13,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent=self, debug=False
        )
        self.motor11TemperatureLabel = GradientWarningDoubleDisplayLabel(
            "11 Temp", "Motors", "11Temperature",
            (153, 215, 189), (243, 95, 0),
            10, 50,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent=self, debug=False
        )
        self.updateButton = QPushButton("Update")
        self.updateButton.setStyleSheet("color: white; font-weight: bold; font-size: 20px;")
        self.updateButton.clicked.connect(self.updateLabels)
        layout = QVBoxLayout(self)
        layout.addWidget(self.motor10CurrentLabel)
        layout.addWidget(self.motor10VoltageLabel)
        layout.addWidget(self.motor10TemperatureLabel)
        layout.addWidget(self.motor11CurrentLabel)
        layout.addWidget(self.motor11VoltageLabel)
        layout.addWidget(self.motor11TemperatureLabel)
        layout.addWidget(self.updateButton)


    def updateLabels(self):
        self.motor10CurrentLabel.manualUpdate()
        self.motor10VoltageLabel.manualUpdate()
        self.motor10TemperatureLabel.manualUpdate()
        self.motor11CurrentLabel.manualUpdate()
        self.motor11VoltageLabel.manualUpdate()
        self.motor11TemperatureLabel.manualUpdate()