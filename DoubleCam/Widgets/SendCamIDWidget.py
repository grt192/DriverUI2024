from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, \
    QGroupBox, QSizePolicy
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, SignalInstance, Slot, Signal
from DoubleCam.Helpers.NetworktableHelper import NetworkTableManager


class SendCamIDWidget(QWidget):

    message = None
    def __init__(self, parameterName, tableName, entryName, parent=None):
        super().__init__(parent)

        self.parameterName = parameterName
        # Set NTManager
        self.tableName = tableName
        self.entryName = entryName

        self.NTManager1 = NetworkTableManager(table_name=tableName, entry_name=entryName)
        self.cnt = 2
        # Create widgets
        self.groupBox = QGroupBox(self)

        self.label = QLabel(self.parameterName, self.groupBox)
        self.label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.button = QPushButton(self.parameterName, self.groupBox)
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set up layout
        self.layout = QVBoxLayout(self.groupBox)
        self.layout.addWidget(
            self.label, alignment=Qt.AlignmentFlag.AlignCenter
        )  # Center the label
        self.layout.addWidget(self.button)

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.groupBox)

        # Connect the clicked signal to the toggle method
        self.button.clicked.connect(self.sendInt)

        # Update the button appearance

    def sendInt(self):
        if self.cnt is None:
            raise Exception("Message is None")
        # Toggle the boolean value and update the button
        #Update State

        self.sendNTValue()
        if self.cnt == 1:
            self.cnt = 2
        else:
            self.cnt = 1

    def sendNTValue(self):
        self.NTManager1.putInt(self.cnt)
