import sys
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QComboBox, QPushButton, QMessageBox, QGroupBox
from PySide6.QtCore import Qt, QTimer


class AutonChooserWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        self.auton_options = ["Option 1", "Option 2", "Option 3"]  # Modify as per your requirement
        self.auton_dropdown = QComboBox()
        self.auton_dropdown.addItems(self.auton_options)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_selection)

        layout.addWidget(self.auton_dropdown)
        layout.addWidget(self.confirm_button)

        self.group_box = QGroupBox("Auton Chooser")
        self.group_box.setLayout(layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.group_box)
        self.setLayout(main_layout)

    def confirm_selection(self):
        selected_option = self.auton_dropdown.currentText()
        # QMessageBox.information(self, "Selection Confirmed", f"Auton Option '{selected_option}' confirmed!", QMessageBox.Ok)
        self.auton_dropdown.setStyleSheet("background-color: lightgreen;")
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset_color)
        self.timer.start(1000)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)
        
        # self.setStyleSheet("background-color: lightgreen;")

    def reset_color(self):
        self.auton_dropdown.setStyleSheet("background-color: none;")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = AutonChooserWidget()
    widget.show()
    sys.exit(app.exec())
