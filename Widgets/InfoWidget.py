from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from Widgets.BaseWidgets.BoolDisplayLabel import BoolDisplayLabel
from Widgets.BaseWidgets.IntDisplayLabel import IntDisplayLabel
from Widgets.BaseWidgets.DoubleDisplayLabel import DoubleDisplayLabel
from Widgets.BaseWidgets.ConnectionDisplayLabel import ConnectionDisplayLabel
from Helpers.NetworktableManager import NetworkTableManager

class InfoWidget(QWidget):
    allianceColorChanged = Signal((str))

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.isRedAllianceNTM = NetworkTableManager("FMSInfo", "IsRedAlliance")
        # self.isRedAllianceNTM.new_value_available.connect(self.updateAllianceColor)
        #
        # self.stationNumberNTM = NetworkTableManager("FMSInfo", "StationNumber")
        # self.stationNumberNTM.new_value_available.connect(self.updateMatchNumber)
        #
        # self.matchNumberNTM = NetworkTableManager("FMSInfo", "MatchNumber")
        # self.matchNumberNTM.new_value_available.connect(self.updateMatchNumber)
        #
        # self.allianceLabel = QLabel(self)
        # self.allianceLabel.setMaximumHeight(50)
        # self.allianceLabel.setAlignment(Qt.AlignCenter)
        self.isRedAlliance = None
        # self.stationNumber = None
        #
        # self.matchLabel = QLabel(self)
        # self.matchLabel.setMaximumHeight(50)
        # self.matchLabel.setAlignment(Qt.AlignCenter)
        # self.matchNumber = None

        self.allianceLabel= BoolDisplayLabel("Alliance", "FMSInfo", "IsRedAlliance", "red", "blue", self)
        self.stationLabel= IntDisplayLabel("Station: ", "FMSInfo", "StationNumber", self)
        self.matchLabel = IntDisplayLabel("Match: ", "FMSInfo", "MatchNumber", self)
        self.elevatorExtensionPercentLabel = DoubleDisplayLabel("Elevator%: ", "Elevator", "ExtensionPercent", self)
        self.elevatorLimitSwitchLabel = BoolDisplayLabel("ElevatorLS", "Elevator", "LimitSwitch", "green", "red", self)
        self.motor10CurrentLabel = DoubleDisplayLabel("10 Current: ", "Motors", "10Current", self)
        self.motor10VoltageLabel = DoubleDisplayLabel("10 Voltage: ", "Motors", "10Voltage", self)
        self.motor10TemperatureLabel = DoubleDisplayLabel("10 Temp: ", "Motors", "10Temperature", self)
        self.motor11CurrentLabel = DoubleDisplayLabel("11 Current: ", "Motors", "11Current", self)
        self.motor11VoltageLabel = DoubleDisplayLabel("11 Voltage: ", "Motors", "11Voltage", self)
        self.motor11TemperatureLabel = DoubleDisplayLabel("11 Temp: ", "Motors", "11Temperature", self)
        # self.AMPRockwellLabel = BoolDisplayLabel("AMPSensor", "Intake", "AMP", "green", "red", self)
        self.visionConnectionLabel = ConnectionDisplayLabel("Vision", "http://10.1.92.13:5800", self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.allianceLabel)
        layout.addWidget(self.stationLabel)
        layout.addWidget(self.matchLabel)
        layout.addWidget(self.elevatorExtensionPercentLabel)
        layout.addWidget(self.elevatorLimitSwitchLabel)
        layout.addWidget(self.motor10CurrentLabel)
        layout.addWidget(self.motor10VoltageLabel)
        layout.addWidget(self.motor10TemperatureLabel)
        layout.addWidget(self.motor11CurrentLabel)
        layout.addWidget(self.motor11VoltageLabel)
        layout.addWidget(self.motor11TemperatureLabel)
        # layout.addWidget(self.AMPRockwellLabel)
        layout.addWidget(self.visionConnectionLabel)
