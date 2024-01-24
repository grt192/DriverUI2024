from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QGroupBox, QSizePolicy
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, SignalInstance, Slot, Signal
from Helpers.NetworktableHelper import NetworkTableManager


class ToggleWidget(QWidget):
    send_to_nt = Signal(str, object)
    toggled = Signal(str)
    
    def __init__(self, parameter_name, table_name, entry_name, states=None, colors=None, initial_value=False, able_to_toggle=True, parent=None):
        super().__init__(parent)

        # Set the initial value and update the button text and background color
        self.current_state = initial_value
        self.parameter_name = parameter_name
        self.nt_name = entry_name # Network Table entry name
        print("ToggleWidget table name: " + table_name + "Entry name: " + entry_name)
        self.nt_manager = NetworkTableManager(table_name=table_name, entry_name=entry_name)
        self.nt_manager.new_value_available.connect(self.update_nt_value)
        
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
        
        self.able_to_toggle = able_to_toggle
        if not self.able_to_toggle:
            self.setEnabled(False)

        # Connect the clicked signal to the toggle method
        self.button.clicked.connect(self.toggle)

        # Update the button appearance
        self.update_button()

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.group_box)

    def toggle(self):
        print("toggle is called")
        # Toggle the boolean value and update the button
        self.current_state = not self.current_state
        self.text_value = str(self.current_state)
        self.text_value = self.text_value.lower()
        self.update_button()
        self.sendNTValue()
        self.toggled.emit(self.current_state)


    def update_button(self):
        # Update the button text and background color based on the boolean value
        self.button.setText(str(self.text_value))
        color = QColor(self.true_color if self.current_state else self.false_color)
        self.button.setStyleSheet(f"background-color: {color.name()};")
        self.button.setAutoFillBackground(True)

    @Slot(str, object)
    def update_nt_value(self, key:str, value:object):
        print(f"key {key}, value {value}")
        if not self.able_to_toggle:
            self.current_state = value
        else:
            self.current_state = key

    def sendNTValue(self):
        if type(self.current_state) is bool:
            self.nt_manager.putBool(self.current_state)
        elif type(self.current_state) is str:
            self.nt_manager.putString(str(self.current_state).lower())
        return;