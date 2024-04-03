from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QPushButton
from Widgets.CustomWidgets.BaseWidgets.BoolDisplayLabel import BoolDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.IntDisplayLabel import IntDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.DoubleDisplayLabel import DoubleDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.ConnectionDisplayLabel import ConnectionDisplayLabel
from Widgets.CustomWidgets.AllianceLabel import AllianceLabel
from Widgets.CustomWidgets.BaseWidgets.GradientDoubleDisplayLabel import GradientDoubleDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.GradientWarningDoubleDisplayLabel import GradientWarningDoubleDisplayLabel

class InfoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.timer = QTimer()
        self.timer.start(500)
        self.allianceLabel = AllianceLabel(self)
        self.timeLeftLabel = GradientWarningDoubleDisplayLabel(
            "Time", "FMS", "TimeLeft",
            (255, 105, 0), (255, 219, 194),
            20., 135,
            self.timer,
            parent = self, debug = False
        )
        self.elevatorExtensionPercentLabel = GradientDoubleDisplayLabel(
            "Elevator%", "Elevator", "ExtensionPercent",
            (214, 157, 250),(157, 0, 255),
            0., 1.,
            "color: white; font-weight: bold; font-size: 20px;",
            parent = self, debug = False
        )
        self.elevatorLimitSwitchLabel = BoolDisplayLabel(
            "ElevatorLS", "Elevator", "LimitSwitch",
            (1, 188, 70),(254, 66, 30),
            parent = self, debug = True
        )
        self.motor10CurrentLabel = GradientWarningDoubleDisplayLabel(
            "10 Current", "Motors", "10Current",
            (0,180, 70), (1, 181, 71),
            0, 40,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent = self, debug = False
        )
        self.motor10VoltageLabel = GradientWarningDoubleDisplayLabel(
            "10 Voltage: ", "Motors", "10Voltage",
            (0, 180, 70), (1, 181, 71),
            12, 13,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent = self, debug = False
        )

        self.motor10TemperatureLabel = GradientWarningDoubleDisplayLabel(
            "10 Temp", "Motors", "10Temperature",
            (153, 215, 189), (243, 95, 0),
            10, 50,
            self.timer,
            "color: white; font-weight: bold; font-size: 20px;",
            parent = self, debug = False
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
            parent=self, debug= False
        )
        self.visionConnectionLabel = ConnectionDisplayLabel(
            "Vision", "http://10.1.92.13:5800",
            (0,180,70), (255, 0, 0),
            "color: white; font-weight: bold; font-size: 16px;",
            parent = self
        )
        self.ampSensorLabel = BoolDisplayLabel(
            "AMP Sensor", "Intake", "AMPSensor",
            (0, 255, 0), (255, 0, 0),
            parent=self
        )
        self.frontSensorLabel = BoolDisplayLabel(
            "Front Sensor", "Intake", "FrontSensor",
            (0,255,0), (255, 0, 0),
            parent = self
        )
        self.rockwellSensorLabel = BoolDisplayLabel(
            "R Sensor", "Intake", "Rockwell",
            (0, 255, 0), (255, 0, 0),
            parent=self
        )
        self.updateButton = QPushButton("Update")
        self.updateButton.setStyleSheet("color: white; font-weight: bold; font-size: 20px;")
        self.updateButton.clicked.connect(self.updateLabels)

        layout = QVBoxLayout(self)
        layout.addWidget(self.allianceLabel)
        layout.addWidget(self.timeLeftLabel)
        layout.addWidget(self.elevatorExtensionPercentLabel)
        layout.addWidget(self.elevatorLimitSwitchLabel)
        layout.addWidget(self.motor10CurrentLabel)
        layout.addWidget(self.motor10VoltageLabel)
        layout.addWidget(self.motor10TemperatureLabel)
        layout.addWidget(self.motor11CurrentLabel)
        layout.addWidget(self.motor11VoltageLabel)
        layout.addWidget(self.motor11TemperatureLabel)
        layout.addWidget(self.visionConnectionLabel)
        layout.addWidget(self.ampSensorLabel)
        layout.addWidget(self.frontSensorLabel)
        layout.addWidget(self.rockwellSensorLabel)
        layout.addWidget(self.updateButton)

    def updateLabels(self):
        self.allianceLabel.manualUpdate()
        self.timeLeftLabel.manualUpdate()
        self.elevatorExtensionPercentLabel.manualUpdate()
        self.elevatorLimitSwitchLabel.manualUpdate()
        self.motor10CurrentLabel.manualUpdate()
        self.motor10VoltageLabel.manualUpdate()
        self.motor10TemperatureLabel.manualUpdate()
        self.motor11CurrentLabel.manualUpdate()
        self.motor11VoltageLabel.manualUpdate()
        self.motor11TemperatureLabel.manualUpdate()
        self.visionConnectionLabel.updateConnectionStatus()
