from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt
from Helpers.NetworktableManager import NetworkTableManager


class DoubleDisplayLabel(QLabel):

    def __init__(self, parameterName, tableName, entryName, parent = None):
        super().__init__(parameterName, parent)

        self.parameterName = parameterName
        self.tableName = tableName
        self.entryName = entryName

        self.NTManager = NetworkTableManager(
            tableName=tableName, entryName=entryName
        )
        self.NTManager.new_value_available.connect(self.updateFromNT)

        if self.NTManager.getValue() is not None:
            self.updateFromNT(("init", self.NTManager.getValue()))
            self.setStyleSheet(f"background-color: black; color: red;")
        else:
            self.setStyleSheet(f"background-color: gray;")
            self.setText("No Data")

        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)

    def updateFromNT(self, message: tuple):
        self.setText(self.parameterName + str(float(message[1])))