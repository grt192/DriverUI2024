import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QSizePolicy, QGroupBox

class ControlWidget(QWidget):
    alliance_color_changed = Signal((str))
    
    def __init__(self):
        super().__init__()


    def emit_color_changed_signal(self, new_alliance_color):
        self.alliance_color_changed.emit(new_alliance_color)
        
    def lock_alliance(self, lock_state):
        if lock_state == 'locked':
            self.alliance_color_toggle.setEnabled(False)
        else:
            self.alliance_color_toggle.setEnabled(True)
