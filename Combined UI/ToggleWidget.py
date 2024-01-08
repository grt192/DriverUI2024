from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QGroupBox
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class ToggleWidget(QWidget):
    def __init__(self, parameter_name, initial_value=False, parent=None):
        super().__init__(parent)

        # Set the initial value and update the button text and background color
        self.value = initial_value
        self.parameter_name = parameter_name

        # Create widgets
        self.group_box = QGroupBox(self)
        self.label = QLabel(self.parameter_name, self.group_box)
        self.button = QPushButton(str(self.value), self.group_box)

        # Set up layout
        self.layout = QVBoxLayout(self.group_box)
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the label
        self.layout.addWidget(self.button)

        # Connect the clicked signal to the toggle method
        self.button.clicked.connect(self.toggle)

        # Update the button appearance
        self.update_button()

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.group_box)

    def toggle(self):
        # Toggle the boolean value and update the button
        self.value = not self.value
        self.update_button()

    def update_button(self):
        # Update the button text and background color based on the boolean value
        self.button.setText(str(self.value))
        color = QColor("green" if self.value else "red")
        self.button.setStyleSheet(f"background-color: {color.name()};")
        self.button.setAutoFillBackground(True)
