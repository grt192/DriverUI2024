from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from Helpers.NetworktableManager import NetworkTableManager


class StringDisplayLabel(QLabel):

    def __init__(
        self, parameterName, tableName, entryName,
        generalStyleSheet: str = "color: white; font-weight: bold; font-size: 30px;",
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
        self.generalStyleSheet = generalStyleSheet
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.manualUpdate()

    def updateFromNT(self, message: tuple):
        self.setText(self.parameterName + message[1])
        self.setStyleSheet(self.generalStyleSheet)

    def manualUpdate(self):
        if (self.NTManager.getValue() != None):
            self.updateFromNT(("init", self.NTManager.getValue()))
        else:
            self.setStyleSheet(f"background-color: gray;" + self.generalStyleSheet)
            self.setText("No Data")
            print("str no")