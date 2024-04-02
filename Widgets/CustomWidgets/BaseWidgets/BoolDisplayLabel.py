from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from Helpers.NetworktableManager import NetworkTableManager


class BoolDisplayLabel(QLabel):

    def __init__(
        self, parameterName, tableName, entryName,
        trueColor: tuple, falseColor: tuple, generalStyleSheet: str = "color: white; font-weight: bold; font-size: 30px;",
        parent = None, debug = False
    ):
        super().__init__(parameterName, parent)
        self.parameterName = parameterName
        self.tableName = tableName
        self.entryName = entryName
        self.NTManager = NetworkTableManager(
            tableName=tableName, entryName=entryName
        )
        self.NTManager.new_value_available.connect(self.updateFromNT)
        self.trueColor = trueColor
        self.falseColor = falseColor
        self.trueColorText = "rgb" + str(trueColor)
        self.falseColorText = "rgb" + str(falseColor)
        self.generalStyleSheet = generalStyleSheet
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.manualUpdate()

    def updateFromNT(self, message: tuple):
        if message[1]:
            self.setStyleSheet("background-color: rgb" + str(self.trueColor) + ";" + self.generalStyleSheet)
            self.setText(self.parameterName)
        else:
            self.setStyleSheet("background-color: rgb" + str(self.falseColor) + ";" + self.generalStyleSheet)
            self.setText(self.parameterName)

    def manualUpdate(self):
        print(self.entryName)
        if (self.NTManager.getValue() != None):
            self.updateFromNT(("init", self.NTManager.getValue()))
        else:
            self.setStyleSheet(f"background-color: gray;" + self.generalStyleSheet)
            self.setText("No Data")