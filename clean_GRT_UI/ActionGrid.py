import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from ActionWidget import ActionWidget

class ActionGrid(QWidget):
    def __init__(self, actions_info, parent=None):
        super().__init__(parent)

        # Create a grid layout
        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(0)  # Adjust the spacing between widgets
        self.action_toggles = []

        # Create ActionWidgets based on the provided information and add them to the grid layout
        for action_info in actions_info:
            row = action_info.get("row", 0)
            col = action_info.get("col", 0)
            action_widget = ActionWidget(**action_info, table_name="table name", entry_name="entry name")
            self.action_toggles.append(action_widget)
            self.grid_layout.addWidget(action_widget, row, col)
            
    def change_alliance_color(self, new_alliance_color):
        for widget in self.action_toggles:
            widget.change_alliance_color(new_alliance_color)

# EXAMPLE USAGE:
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Define a list of dictionaries with ActionWidget parameters and positions
    actions_info = [
        {"action_name": "Action 1", "table_name":'', "entry_name": '', "alliance": "red", "row": 0, "col": 0},
        {"action_name": "Action 2", "table_name":'', "entry_name": '', "alliance": "blue", "row": 0, "col": 1},
        {"action_name": "Action 3", "table_name":'', "entry_name": '', "alliance": "red", "row": 0, "col": 2},
        {"action_name": "Action 4", "table_name":'', "entry_name": '', "alliance": "blue", "row": 1, "col": 0},
        {"action_name": "Action 5", "table_name":'', "entry_name": '', "alliance": "red", "row": 1, "col": 1},
        {"action_name": "Action 6", "table_name":'', "entry_name": '', "alliance": "blue", "row": 1, "col": 2},
    ]

    action_grid = ActionGrid(actions_info)
    action_grid.setWindowTitle("ActionWidget Grid")
    action_grid.resize(600, 400)
    action_grid.show()
    
    sys.exit(app.exec())
