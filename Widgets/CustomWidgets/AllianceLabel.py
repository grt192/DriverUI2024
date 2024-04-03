from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt, Signal
from Helpers.NetworktableManager import NetworkTableManager


class AllianceLabel(QLabel):
    isRedSignal = Signal(bool)
    def __init__(self, parent = None):
        super().__init__(parent)
        self.allianceColorNTManager = NetworkTableManager(tableName ="FMSInfo", entryName ="IsRedAlliance")
        self.allianceColorNTManager.new_value_available.connect(self.updateAllianceColor)
        self.isRedAlliance = None
        self.stationNumber = None
        self.stationNumberNTManager = NetworkTableManager(tableName ="FMSInfo", entryName ="StationNumber")
        self.stationNumberNTManager.new_value_available.connect(self.updateStationNumber)
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.generalStyleSheet = "color: white;"\
            "font-weight: bold; font-size: 40px;"

        self.manualUpdate()

    def updateAllianceColor(self, message: tuple):
        if message[1]:
            if self.stationNumber != None:
                self.setText("Red " + str(int(self.stationNumber)))
            self.setStyleSheet("background-color: rgb(254, 66, 30);" + self.generalStyleSheet)
            self.isRedAlliance = True
            self.isRedSignal.emit(True)
        else:
            if self.stationNumber != None:
                self.setText("Blue " + str(int(self.stationNumber)))
            self.setStyleSheet("background-color: rgb(1,90,188);" + self.generalStyleSheet)
            self.isRedAlliance = False
            self.isRedSignal.emit(False)


    def updateStationNumber(self, message: tuple):
        text = "? "
        if message[1] != None:
            if self.isRedAlliance != None:
               if self.isRedAlliance:
                   text = "Red "
               else:
                   text = "Blue "
            self.setText(text + str(int(message[1])))
            self.stationNumber = message[1]
        else:
            self.setText("No Data")

    def manualUpdate(self):
        if (self.allianceColorNTManager.getValue() != None):
            self.updateAllianceColor(("init", self.allianceColorNTManager.getValue()))
        else:
            self.setStyleSheet("background-color: gray;" )
        if(self.stationNumberNTManager.getValue() != None):
            self.updateStationNumber(("init", self.stationNumberNTManager.getValue()))
        else:
            self.setText("No Data")