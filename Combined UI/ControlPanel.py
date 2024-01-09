import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QSizePolicy, QGroupBox
from ToggleWidget import ToggleWidget
from TelemWidget import TelemWidget

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets for the control panel
        label1 = QLabel("Text Input 1:")
        text_input1 = QLineEdit(self)

        label2 = QLabel("Dropdown:")
        dropdown = QComboBox(self)
        dropdown.addItems(["Option 1", "Option 2", "Option 3"])

        checkbox = QCheckBox("Check me", self)

        label3 = QLabel("Text Input 2:")
        text_input2 = QLineEdit(self)

        # Create a vertical layout for the control panel
        layout = QVBoxLayout(self)
        layout.addWidget(label1)
        layout.addWidget(text_input1)
        layout.addWidget(label2)
        layout.addWidget(dropdown)
        layout.addWidget(checkbox)
        layout.addWidget(label3)
        layout.addWidget(text_input2)
        layout.addWidget(ToggleWidget("Alliance", states=('Red', 'Blue'), colors=('red','blue')))
        layout.addWidget(TelemWidget("test"))
        layout.addStretch()  # Adds stretchable space at the end

        # Set the size policy and maximum width for the control panel
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.setMaximumWidth(300)  # Set the maximum width as needed

        # Create a group box and set the layout
        group_box = QGroupBox("")
        group_box.setLayout(layout)

        # Set the layout for the main widget
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication

#     class MainApp(QApplication):
#         def __init__(self, argv):
#             super(MainApp, self).__init__(argv)
#             self.main_window = ControlPanel()
#             self.main_window.show()

#     app = MainApp(sys.argv)
#     sys.exit(app.exec())
