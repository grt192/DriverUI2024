from PySide6.QtWidgets import QGridLayout, QWidget, QMainWindow
from ToggleWidget import ToggleWidget

class ToggleGrid(QWidget):
    def __init__(self, toggle_data, parent=None):
        super().__init__(parent)

        # Set up the grid layout
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)  # Adjust the spacing between widgets

        # Create ToggleWidgets based on the toggle_data provided in the constructor
        for toggle_info in toggle_data:
            row = toggle_info.get("row", 0)
            col = toggle_info.get("col", 0)
            able_to_toggle = toggle_info.get("able_to_toggle", True)
            table_name = toggle_info.get('table_name', '')
            nt_name = toggle_info.get('nt_name', '')
            toggle_widget = ToggleWidget(parameter_name=toggle_info.get("name", ""),
                                         table_name=table_name,
                                         entry_name=nt_name,
                                         initial_value=toggle_info.get("value", False),
                                         states=toggle_info.get("states", None),
                                         colors=toggle_info.get("colors", None),
                                         able_to_toggle=able_to_toggle,
                                         parent=self)
            self.grid_layout.addWidget(toggle_widget, row, col)

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

            toggle_data = [
                {"name": "Toggle 1", "value": True, "row": 0, "col": 0},
                {"name": "Toggle 2", "value": False, "row": 0, "col": 1},
                {"name": "Toggle 3", "value": True, "row": 0, "col": 2},
                {"name": "Toggle 4", "value": False, "row": 1, "col": 0},
                {"name": "Toggle 5", "value": True, "row": 1, "col": 1},
                {"name": "Toggle 6", "value": False, "row": 1, "col": 2},
                {"name": "Toggle 7", "value": True, "row": 2, "col": 0},
                {"name": "Toggle 8", "value": False, "row": 2, "col": 1},
                {"name": "Toggle 9", "value": True, "row": 2, "col": 2},
            ]

            self.toggle_grid = ToggleGrid(toggle_data)
            self.setCentralWidget(self.toggle_grid)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
