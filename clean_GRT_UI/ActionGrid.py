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

        self.num_widgets = len(actions_info)
        
        # Create ActionWidgets based on the provided information and add them to the grid layout
        for index, action_info in enumerate(actions_info):
            action_widget = ActionWidget(**action_info)
            self.action_toggles.append(action_widget)
            self.grid_layout.addWidget(action_widget, index // 3, index % 3)
            
    def change_alliance_color(self, new_alliance_color):
        for i in range(self.num_widgets):
            # widget = self.grid_layout.itemAt(i)
            widget = self.action_toggles[i]
            # print(widget)
            widget.change_alliance_color(new_alliance_color)

# EXAMPLE USAGE:
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Define a list of dictionaries with ActionWidget parameters
    actions_info = [
        {"action_name": "Action 1", "alliance": "red"},
        {"action_name": "Action 2", "alliance": "blue"},
        {"action_name": "Action 3", "alliance": "red"},
        {"action_name": "Action 4", "alliance": "blue"},
        {"action_name": "Action 5", "alliance": "red"},
        {"action_name": "Action 6", "alliance": "blue"},
    ]

    action_grid = ActionGrid(actions_info)
    action_grid.setWindowTitle("ActionWidget Grid")
    action_grid.resize(600, 400)
    action_grid.show()
    
    sys.exit(app.exec())
