from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QGroupBox, QComboBox, QRadioButton, QCheckBox
from PySide6.QtGui import QColor
from PySide6.QtCore import *

class AllianceToggleWidget(QCheckBox):
    def __init__(self, alliance, mainWindowDelegate):
        super().__init__()

        self.alliance = alliance
        self.mainWindowDelegate = mainWindowDelegate
        AllianceSwitchStyleSheetFile = QFile("./AllianceSwitch.qss")
        AllianceSwitchStyleSheetFile.open(QFile.OpenModeFlag.ReadOnly)
        AllianceSwitchStyleSheet = AllianceSwitchStyleSheetFile.readAll().toStdString()
        self.setStyleSheet(AllianceSwitchStyleSheet)

    def toggle(self):
        # Toggle the boolean value and update the button
        if self.isChecked():
            self.alliance = 'blue'
        else:
            self.alliance = 'red'
        #Call other Update Method
