from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from Helpers.NetworktableHelper import NetworkTableManager


class RobotStatusWidget(QWidget):
    trueColor = QColor("Green")
    falseColor = QColor("Red")

    def __init__(self, name, ntTableName, ntEntryName):
        super(RobotStatusWidget, self).__init__()
        self.currentState = False
        self.label = QLabel(name)
        self.label.setAlignment(Qt.AlignCenter)
        self.ntManager = NetworkTableManager(ntTableName, ntEntryName)
        self.ntManager.new_value_available.connect(self.updateValue)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.setAutoFillBackground(True)
        self.setMinimumHeight(50)
    def updateLabel(self):
        if self.currentState:
            self.label.setStyleSheet(f"background-color: {self.trueColor.name()};")
        elif self.currentState is False:
            self.label.setStyleSheet(f"background-color: {self.falseColor.name()};")

    def updateValue(self, value: tuple):
        print(value)
        self.currentState = value[1]
        self.updateLabel()
