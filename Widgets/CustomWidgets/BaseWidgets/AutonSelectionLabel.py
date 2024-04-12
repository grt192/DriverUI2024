from PySide6.QtWidgets import QLabel, QComboBox, QVBoxLayout
from Helpers.NetworktableManager import NetworkTableManager
class AutonSelectionLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selectionNTManager = NetworkTableManager("Auton", "Auton")
        self.listNTManager = NetworkTableManager("Auton", "AutonList")
        self.listNTManager.new_value_available.connect(self.updateList)
        self.combo = QComboBox()
        self.combo.currentIndexChanged.connect(self.update)
        self.combo.setStyleSheet("color: white; font-weight: bold; font-size: 12px; background-color: black")
        # print(list(self.listNTManager.getValue()).sort())
        sortedList = list(self.listNTManager.getValue())
        sortedList.sort()
        self.combo.addItems(tuple(sortedList))
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.combo)
        self.setLayout(self.layout)
    def update(self):
        self.selectionNTManager.putString(self.combo.currentText())
    def updateList(self, message: tuple):
        self.combo.clear()
        self.combo.addItems(message[1])