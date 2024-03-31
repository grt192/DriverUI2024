from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt
from Helpers.NetworktableManager import NetworkTableManager


class BoolDisplayLabel(QLabel):

    def __init__(self, parameterName, tableName, entryName, trueColor, falseColor, parent = None):
        super().__init__(parameterName, parent)
        self.NTManager = NetworkTableManager(
            tableName=tableName, entryName=entryName
        )
        self.NTManager.new_value_available.connect(self.updateFromNT)
        self.trueColor = trueColor
        self.falseColor = falseColor
        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        if(self.NTManager.getValue() is not None):
            self.updateFromNT(("init", self.NTManager.getValue()))
        else:
            self.setStyleSheet(f"background-color: gray;")
            self.setText("No Data")

    def updateFromNT(self, message: tuple):
        if message[1]:
            self.setStyleSheet(f"background-color: " + self.trueColor + ";")
        else:
            self.setStyleSheet(f"background-color: " + self.falseColor + ";")