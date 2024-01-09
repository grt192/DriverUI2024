import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
from ActionWidget import ActionWidget

class ActionGrid(QWidget):
    def __init__(self, actions_info, parent=None):
        super().__init__(parent)

        self.setWindowTitle("ActionWidget Grid Example")
        self.resize(600, 400)

        # Create a grid layout
        grid_layout = QGridLayout(self)

        # Create ActionWidgets based on the provided information and add them to the grid layout
        for row, action_info in enumerate(actions_info):
            action_widget = ActionWidget(**action_info)
            grid_layout.addWidget(action_widget, row // 3, row % 3)

# EXAMPLE USAGE:
# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Define a list of dictionaries with ActionWidget parameters
#     actions_info = [
#         {"action_name": "Action 1", "alliance": "red"},
#         {"action_name": "Action 2", "alliance": "blue"},
#         {"action_name": "Action 3", "alliance": "red"},
#         {"action_name": "Action 4", "alliance": "blue"},
#         {"action_name": "Action 5", "alliance": "red"},
#         {"action_name": "Action 6", "alliance": "blue"},
#     ]

#     action_grid = ActionGrid(actions_info)
#     action_grid.show()

#     sys.exit(app.exec())
