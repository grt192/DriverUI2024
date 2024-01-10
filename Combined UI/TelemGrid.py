from PySide6.QtWidgets import QGridLayout, QWidget, QMainWindow
from TelemWidget import TelemWidget

class TelemGrid(QWidget):
    def __init__(self, telem_data, parent=None):
        super().__init__(parent)

        # Set up the grid layout
        self.grid_layout = QGridLayout(self)
        # self.grid_layout.setSpacing(10)  # Adjust the spacing between widgets

        # Create TelemWidgets based on the provided telem_data
        for row in range(3):
            for col in range(3):
                telem_info = telem_data[row * 3 + col]
                telem_widget = TelemWidget(label=telem_info.get("name", ""),
                                           initial_value=telem_info.get("value", "N/A"),
                                           parent=self)
                self.grid_layout.addWidget(telem_widget, row, col)

        # Set up main layout
        # self.main_layout = QGridLayout(self)
        # self.main_layout.addLayout(self.grid_layout, 0, 0)
        

# Example usage
# if __name__ == "__main__":
#     import sys
#     from PySide6.QtWidgets import QApplication

#     class MainWindow(QMainWindow):
#         def __init__(self):
#             super().__init__()

#             telem_data = [
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"},
#                 {"name": "Quantity", "value": "0.00"}
#             ]

#             self.telem_grid = TelemGrid(telem_data)
#             self.setCentralWidget(self.telem_grid)

#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
