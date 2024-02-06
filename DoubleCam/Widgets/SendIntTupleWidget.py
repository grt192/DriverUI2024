from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, \
    QGroupBox, QSizePolicy
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, SignalInstance, Slot, Signal
from Helpers.NetworktableHelper import NetworkTableManager


class SendIntTupleWidget(QWidget):

    message = None
    def __init__(self, parameterName, table1Name, entry1Name, table2Name, entry2Name, parent=None):
        super().__init__(parent)

        self.parameterName = parameterName
        # Set NTManager
        self.table1Name = table1Name
        self.entry1Name = entry1Name
        self.table2Name = table2Name
        self.entry2Name = entry2Name

        self.NTManager1 = NetworkTableManager(table_name=table1Name, entry_name=entry1Name)
        self.NTManager2 = NetworkTableManager(table_name=table2Name, entry_name=entry2Name)

        self.trueText = "Send"
        self.falseText = "Sending..."

        # Update current text
        self.currentState = False
        self.currentText = self.falseText

        # Set Colors for states
        colors = ('green', 'red')
        self.trueColor = colors[0]
        self.falseColor = colors[1]
        self.currentColor = self.falseColor

        # Create widgets
        self.groupBox = QGroupBox(self)

        self.label = QLabel(self.parameterName, self.groupBox)
        self.label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.button = QPushButton(self.currentText, self.groupBox)
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
        self.button.clicked.connect(self.sendIntTuple)

        # Update the button appearance
        self.flipState()

    @Slot(tuple)
    def updateMessage(self, message:(int, int)):
        self.message = message

    def sendIntTuple(self):
        if self.message is None:
            raise Exception("Message is None")
        # Toggle the boolean value and update the button
        #Update State

        self.flipState()
        self.sendNTValue()
        self.flipState()

    def flipState(self):
        # Update the button text and background color based on the boolean value
        self.currentState = not self.currentState #flip state
        #Update Text
        if self.currentState:
            self.currentText = self.trueText
        else:
            self.currentText = self.falseText
        self.button.setText(self.currentText)
        #Update Color
        if self.currentState:
            self.currentColor = self.trueColor
        else:
            self.currentColor = self.falseColor
        self.button.setStyleSheet(f"background-color: {self.currentColor};")
        self.button.setAutoFillBackground(True)

    def sendNTValue(self):
        self.NTManager1.putInt(self.message[0])
        self.NTManager2.putInt(self.message[1])
