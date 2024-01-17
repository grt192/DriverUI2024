from PySide6.QtWidgets import QGridLayout, QWidget, QMainWindow
from TelemWidget import TelemWidget

class TelemGrid(QWidget):
    def __init__(self, telem_data, parent=None):
        super().__init__(parent)

        # Set up the grid layout
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)  # Adjust the spacing between widgets

        # Create TelemWidgets based on the provided telem_data
        for telem_info in telem_data:
            row = telem_info.get("row", 0)
            col = telem_info.get("col", 0)
            telem_widget = TelemWidget(label=telem_info.get("name", ""),
                                       initial_value=telem_info.get("value", "N/A"),
                                       parent=self,
                                       table_name = "table name",
                                       entry_name = "entry name")
            self.grid_layout.addWidget(telem_widget, row, col)

        # Set up main layout
        # self.main_layout = QGridLayout(self)
        # self.main_layout.addLayout(self.grid_layout, 0, 0)

# Example usage
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            telem_data = [
                {"name": "Quantity", "value": "0.00", "row": 0, "col": 0},
                {"name": "Quantity", "value": "0.00", "row": 0, "col": 1},
                {"name": "Quantity", "value": "0.00", "row": 0, "col": 2},
                {"name": "Quantity", "value": "0.00", "row": 1, "col": 0},
                {"name": "Quantity", "value": "0.00", "row": 1, "col": 1},
                {"name": "Quantity", "value": "0.00", "row": 1, "col": 2},
                {"name": "Quantity", "value": "0.00", "row": 2, "col": 0},
                {"name": "Quantity", "value": "0.00", "row": 2, "col": 1},
                {"name": "Quantity", "value": "0.00", "row": 2, "col": 2}
            ]

            self.telem_grid = TelemGrid(telem_data)
            self.setCentralWidget(self.telem_grid)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
