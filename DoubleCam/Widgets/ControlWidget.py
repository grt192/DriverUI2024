import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QLineEdit, QComboBox, QCheckBox, QSizePolicy,
                               QGroupBox)
from Widgets.ToggleWidget import ToggleWidget


class ControlWidget(QWidget):
    allianceColorChanged = Signal((str))

    def __init__(self):
        super().__init__()
        self.allianceToggle = ToggleWidget(
            "Alliance", "", "",
            ("blue", "red"), ("blue", "red")
        )
        self.allianceLock = ToggleWidget(
            "Lock", "", "",
            ("Locked", "Unlocked"), ("red", "green"),
            False
        )
        self.allianceLock.toggled.connect(self.lockAlliance)

        layout = QVBoxLayout(self)
        layout.addWidget(self.allianceToggle)
        layout.addWidget(self.allianceLock)


    def emit_color_changed_signal(self, new_alliance_color):
        self.allianceColorChanged.emit(new_alliance_color)

    def lockAlliance(self, lockState):
        print("lockAlliance:" + lockState)
        if lockState == 'Locked':
            self.allianceToggle.setEnabled(False)
        else:
            self.allianceToggle.setEnabled(True)
