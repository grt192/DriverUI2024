from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from Widgets.ToggleWidget import ToggleWidget
from Helpers.NetworktableHelper import NetworkTableManager

class FMSInfoWidget(QWidget):
    allianceColorChanged = Signal((str))

    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.isRedAllianceNTM = NetworkTableManager("FMSInfo", "IsRedAlliance")
        self.stationNumberNTM = NetworkTableManager("FMSInfo", "StationNumber")
        self.matchNumberNTM = NetworkTableManager("FMSInfo", "MatchNumber")
        self.matchTypeNTM = NetworkTableManager("FMSInfo", "MatchType")

        self.allianceLabel = QLabel(self)
        self.allianceLabel.setMaximumHeight(50)
        self.allianceLabel.setAlignment(Qt.AlignCenter)
        self.isRedAlliance = None
        self.stationNumber = None

        self.matchLabel = QLabel(self)
        self.matchNumber = None
        self.matchType = None

        layout = QVBoxLayout(self)
        layout.addWidget(self.allianceLabel)
        layout.addWidget(self.matchLabel)

        self.isRedAlliance = False
        self.stationNumber = 1
        self.updateAllianceLabel()

    def updateLabels(self):
        self.updateAllianceLabel()
        self.updatematchNumberLabel()
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
        text = None
    def updateAllianceColor(self, entryName, isRedAlliance):
        if entryName == IsRedAlliance:
            self.isRedAlliance = isRedAlliance
            self.updateAllianceLabel()