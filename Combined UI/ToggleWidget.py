from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QGroupBox, QSizePolicy
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

class ToggleWidget(QWidget):
    def __init__(self, parameter_name, states=None, colors=None, initial_value=False, parent=None):
        super().__init__(parent)

        # Set the initial value and update the button text and background color
        self.current_state = initial_value
        self.parameter_name = parameter_name
        
        if states == None: states = ('True', 'False') 
        self.true_state = states[0]
        self.false_state = states[1]
        self.text_value = self.true_state if self.current_state else self.false_state
        
        if colors == None: colors = ('green', 'red')
        self.true_color = colors[0]
        self.false_color = colors[1]

        # Create widgets
        self.group_box = QGroupBox(self)
        self.label = QLabel(self.parameter_name, self.group_box)
        self.button = QPushButton(str(self.current_state), self.group_box)
        
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

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
        self.current_state = not self.current_state
        self.text_value = self.true_state if self.current_state else self.false_state
        self.update_button()

    def update_button(self):
        # Update the button text and background color based on the boolean value
        self.button.setText(str(self.text_value))
        color = QColor(self.true_color if self.current_state else self.false_color)
        self.button.setStyleSheet(f"background-color: {color.name()};")
        self.button.setAutoFillBackground(True)
