from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QPushButton
from Widgets.CustomWidgets.BaseWidgets.BoolDisplayLabel import BoolDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.ConnectionDisplayLabel import ConnectionDisplayLabel
from Widgets.CustomWidgets.AllianceLabel import AllianceLabel
from Widgets.CustomWidgets.BaseWidgets.GradientDoubleDisplayLabel import GradientDoubleDisplayLabel
from Widgets.CustomWidgets.BaseWidgets.GradientWarningDoubleDisplayLabel import GradientWarningDoubleDisplayLabel

class InfoWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.timer = QTimer()
        self.timer.start(100)
        self.allianceLabel = AllianceLabel(self)
        self.timeLeftLabel = GradientWarningDoubleDisplayLabel(
            "Time", "FMS", "TimeLeft",
            (255, 105, 0), (255, 219, 194),
            10., 135,
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

        self.ampSensorLabel = BoolDisplayLabel(
            "AMP Sensor", "Intake", "AMPSensor",
            (0, 255, 0), (255, 0, 0),
            parent=self
        )
        self.frontSensorLabel = BoolDisplayLabel(
            "Front Sensor", "Intake", "FrontSensor",
            (0, 255, 0), (255, 0, 0),
            parent=self
        )
        self.rockwellSensorLabel = BoolDisplayLabel(
            "R Sensor", "Intake", "Rockwell",
            (0, 255, 0), (255, 0, 0),
            parent=self
        )
        self.visionConnectionLabel = ConnectionDisplayLabel(
            "Vision", "http://10.1.92.13:5800",
            (0,180,70), (255, 0, 0),
            "color: white; font-weight: bold; font-size: 16px;",
            parent = self
        )
        self.updateButton = QPushButton("Update")
        self.updateButton.setStyleSheet("color: white; font-weight: bold; font-size: 20px;")
        self.updateButton.clicked.connect(self.updateLabels)

        layout = QVBoxLayout(self)
        layout.addWidget(self.allianceLabel)
        layout.addWidget(self.timeLeftLabel)
        layout.addWidget(self.elevatorExtensionPercentLabel)
        layout.addWidget(self.elevatorLimitSwitchLabel)

        layout.addWidget(self.ampSensorLabel)
        layout.addWidget(self.frontSensorLabel)
        layout.addWidget(self.rockwellSensorLabel)
        layout.addWidget(self.visionConnectionLabel)
        layout.addWidget(self.updateButton)

    def updateLabels(self):
        self.allianceLabel.manualUpdate()
        self.timeLeftLabel.manualUpdate()
        self.elevatorExtensionPercentLabel.manualUpdate()
        self.elevatorLimitSwitchLabel.manualUpdate()
        self.frontSensorLabel.update()
        self.ampSensorLabel.update()
        self.rockwellSensorLabel.update()
        self.visionConnectionLabel.updateConnectionStatus()

