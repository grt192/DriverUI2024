from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QGroupBox, QSizePolicy
from PySide6.QtCore import Qt, Slot, Signal
from Helpers.NetworktableManager import NetworkTableManager


class ToggleWidget(QWidget):
    send_to_nt = Signal(str, object)
    toggled = Signal(str)

    def __init__(
            self, parameterName, tableName, entryName, texts: tuple,
            colors=None, initialState: bool = True, isLocked: bool = False,
            parent=None
    ):
        super().__init__(parent)

        self.parameterName = parameterName

        self.trueText = texts[0]
        self.falseText = texts[1]

        # Update current text
        self.currentState = initialState
        if self.currentState:
            self.currentText = self.trueText
        else:
            self.currentText = self.falseText

        # Set Colors for states
        if colors == None:
            colors = ('green', 'red')
        self.trueColor = colors[0]
        self.falseColor = colors[1]
        self.currentColor = None
        if self.currentState:
            self.currentColor = self.trueColor
        else:
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

        # Lock toggle if needed
        self.isLocked = isLocked
        if self.isLocked:
            self.setEnabled(False)

        # Connect the clicked signal to the toggle method
        self.button.clicked.connect(self.toggle)

        # Update the button appearance
        self.update_button()

    def toggle(self):
        print("toggle is called")
        # Toggle the boolean value and update the button
        self.currentState = not self.currentState
        if self.currentState:
            self.currentText = self.trueText
        else:
            self.currentText = self.falseText
        self.update_button()
        self.toggled.emit(self.currentText)

    def update_button(self):
        # Update the button text and background color based on the boolean value
        #print(self.currentText)
        self.button.setText(self.currentText)
        if self.currentState:
            self.currentColor = self.trueColor
        else:
            self.currentColor = self.falseColor
        self.button.setStyleSheet(f"background-color: {self.currentColor};")
        self.button.setAutoFillBackground(True)