from PySide6.QtWidgets import  QLabel
from PySide6.QtCore import Qt, QTimer
from Helpers.NetworktableManager import NetworkTableManager


class GradientDoubleDisplayLabel(QLabel):

    def __init__(
        self, parameterName: str, tableName: str, entryName: str,
        minColor: tuple[int, int, int], maxColor: tuple[int, int, int],
        minValue: float, maxValue: float,
        generalStyleSheet: str = "color: white; font-weight: bold; font-size: 30px;",
        parent= None, debug = False):
        super().__init__(parameterName, parent)

        self.parameterName = parameterName
        self.tableName = tableName
        self.entryName = entryName

        self.minColor = minColor
        self.maxColor = maxColor
        self.minR = minColor[0]
        self.minG = minColor[1]
        self.minB = minColor[2]
        self.maxR = maxColor[0]
        self.maxG = maxColor[1]
        self.maxB = maxColor[2]
        self.rRange = self.maxR - self.minR
        self.gRange = self.maxG - self.minG
        self.bRange = self.maxB - self.minB
        self.minValue = minValue
        self.maxValue = maxValue
        self.valueRange = self.maxValue - self.minValue
        self.rRatio = self.rRange / self.valueRange
        self.gRatio = self.gRange / self.valueRange
        self.bRatio = self.bRange / self.valueRange

        self.generalStyleSheet = generalStyleSheet
        self.NTManager = NetworkTableManager(
            tableName=tableName, entryName=entryName
        )
        self.NTManager.new_value_available.connect(self.updateFromNT)

        self.setAlignment(Qt.AlignCenter)
        self.setAutoFillBackground(True)
        self.manualUpdate()

        self.debugValue = minValue
        self.debugStep = self.valueRange/1000
        self.debugTimer = QTimer()
        self.debugTimer.timeout.connect(self.debugUpdate)
        if debug:
            self.debugTimer.start(1)
    def updateFromNT(self, message: tuple):
        newValue = float(message[1])
        difference = newValue - self.minValue
        newR = int(self.minR + difference * self.rRatio)
        newG = int(self.minG + difference * self.gRatio)
        newB = int(self.minB + difference * self. bRatio)
        newColorText = "(" + str(newR) + ", " + str(newG) + ", " + str(newB) + ")"
        self.setStyleSheet(self.generalStyleSheet + "background-color: rgb" + newColorText + ";")
        self.setText(self.parameterName + ": " + str("{:.2f}".format(float(message[1]), 2)))


    def manualUpdate(self):
        if self.NTManager.getValue() != None:
            self.updateFromNT(("init", self.NTManager.getValue()))
        else:
            self.setStyleSheet(f"background-color: gray;" + self.generalStyleSheet)
            self.setText("No Data")

    def debugUpdate(self):
        self.updateFromNT(("debug", self.debugValue))
        self.debugValue += self.debugStep
        if self.debugValue > self.maxValue:
            self.debugValue = self.minValue
