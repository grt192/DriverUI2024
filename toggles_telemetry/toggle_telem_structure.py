import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QCheckBox

class CheckBoxExample(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Create a QVBoxLayout
        layout = QVBoxLayout()

        # Create a label to display the status
        self.status_label = QLabel('Check the box to enable a feature.')

        # Create a checkbox
        self.checkbox = QCheckBox('Enable Feature')

        # Connect the stateChanged signal of the checkbox to a custom slot
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)

        # Add widgets to the layout
        layout.addWidget(self.status_label)
        layout.addWidget(self.checkbox)

        # Set the layout for the main window
        self.setLayout(layout)

        # Set up the main window
        self.setWindowTitle('QCheckBox Example')
        self.setGeometry(300, 300, 300, 150)

    def checkbox_state_changed(self, state):
        # Define the behavior when the checkbox state changes
        if state == 2:  # 2 corresponds to Qt.CheckState.Checked
            self.status_label.setText('Feature is enabled.')
        else:
            self.status_label.setText('Feature is disabled.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = CheckBoxExample()
    example.show()
    sys.exit(app.exec())
