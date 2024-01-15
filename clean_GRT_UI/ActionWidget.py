from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QGroupBox, QSizePolicy
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer
from NetworktableHelper2 import NetworkTableManager

class ActionWidget(QWidget):
    def __init__(self, action_name, table_name, entry_name, alliance='red', row=None, col=None, parent=None):
        super().__init__(parent)

        # Set initial properties
        self.action_name = action_name
        self.alliance = alliance
        self.pending = False
        self.cancel = False

        self.nt_manager = NetworkTableManager(table_name=table_name, entry_name=entry_name)
        self.nt_manager.new_value_available.connect(self.update_nt_value)

        # Create widgets
        self.group_box = QGroupBox(self)
        self.label = QLabel(self.action_name, self.group_box)
        self.button = QPushButton(self.action_name, self.group_box)
        self.update_button()
        
        self.button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        # Set up layout
        self.layout = QVBoxLayout(self.group_box)
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the label
        self.layout.addWidget(self.button)

        # Connect the clicked signal to the action method
        self.button.clicked.connect(self.perform_action)

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.group_box)

    def perform_action(self):
        # Perform the robot action
        
        if not self.pending: # Do the action
            self.pending = True
            self.simulate_async_action()
        else: # CANCEL THE ACTION
            self.pending = False
            self.cancel = True
            self.cancel_action()
        
        # self.button.setEnabled(False)
        self.update_button()

    def action_complete(self):
        # Signal that the action is complete
        self.pending = False
        # self.button.setEnabled(True)
        self.update_button()
        
    def cancel_action(self):
        # Simulation, REPLACE
        QTimer.singleShot(500, self.cancel_complete)
    
    def cancel_complete(self):
        self.cancel = False
        self.pending = False
        pass
        
    def simulate_async_action(self):
        
        # Simulate the asynchronous completion after a delay (e.g., 2 seconds)
        # REPLACE
        QTimer.singleShot(2000, self.action_complete)

    def change_alliance_color(self, new_alliance_color):
        self.alliance = new_alliance_color
        self.update_button()
    
    def update_button(self):
        # Update the button text and background color based on the alliance and pending state
        
        color = QColor(self.alliance)
        if self.cancel:
            self.button_text = "CANCELING" 
            color = QColor("orange")
        elif self.pending: 
            self.button_text = "Pending" 
            color = QColor("green")
        else:
            self.button_text = self.action_name
        
        self.button.setText(self.button_text)
        self.button.setStyleSheet(f"background-color: {color.name()};")
        self.button.setAutoFillBackground(True)
        
    def update_nt_value(self, key, value):
        # FIX THIS FIX THIS FIX THIS
        if not self.able_to_toggle:
            self.current_state = value


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QMainWindow
    from PySide6.QtCore import QTimer

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.action_widget = ActionWidget("Action", "red")
            self.setCentralWidget(self.action_widget)
            
            # Simulate an asynchronous action after showing the window
            # QTimer.singleShot(1000, self.simulate_async_action)
            # self.action_widget.clicked.connect(self.simulate_async_action)
            
        def simulate_async_action(self):
            self.action_widget.perform_action()
            
            # Simulate the asynchronous completion after a delay (e.g., 2 seconds)
            QTimer.singleShot(2000, self.action_widget.action_complete)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


