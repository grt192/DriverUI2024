from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from Widgets.BaseWidgets.BoolDisplayLabel import BoolDisplayLabel
from Widgets.BaseWidgets.IntDisplayLabel import IntDisplayLabel
from Widgets.BaseWidgets.DoubleDisplayLabel import DoubleDisplayLabel
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

        layout = QVBoxLayout(self)
        layout.addWidget(self.allianceLabel)
        layout.addWidget(self.stationLabel)
        layout.addWidget(self.matchLabel)
        layout.addWidget(self.elevatorExtensionPercentLabel)

        #self.updateLabels()
    def updateLabels(self):
        self.updateAllianceLabel()
        self.updateMatchLabel()
    def updateAllianceLabel(self):
        text = None
        if self.isRedAlliance:
            text = "Red "
            self.allianceLabel.setStyleSheet(
                "background-color: black; color: red; font-size: 46px;"
            )

        else:
            text ="Blue "
        if self.stationNumber is not None:
            text = text + str(self.stationNumber)
            self.allianceLabel.setStyleSheet(
                "background-color: black; color: blue; font-size: 46px;"
            )
        self.allianceLabel.setText(text)
    def updateMatchLabel(self):
        text = "Match #" + str(int(self.matchNumber))
        self.matchLabel.setText(text)
        self.matchLabel.setStyleSheet(
                "background-color: black; color: red; font-size: 26px;"
        )

    def updateAllianceColor(self, info):
        entryName = info[0]
        isRedAlliance = info[1]
        if entryName == "IsRedAlliance":
            self.isRedAlliance = isRedAlliance
            self.updateAllianceLabel()

    def updateStationNumber(self, info):
        entryName = info[0]
        stationNumber = info[1]
        if entryName == "StationNumber":
            self.stationNumber = stationNumber
            self.updateAllianceLabel()
    def updateMatchNumber(self, info):
        entryName = info[0]
        matchNumber = info[1]
        if entryName == "MatchNumber":
            self.matchNumber = matchNumber
            self.updateMatchLabel()