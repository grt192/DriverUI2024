import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from ToggleGrid import ToggleGrid
from TelemGrid import TelemGrid
from DriverCameraWidget import CameraWidget

class VisionDebugWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        enable_telem_info = [
                {"name": "Enable Telemetry", "value": True , "states": ('Enabled', 'Disabled'), "colors": ('green', 'red'), "row": 0, "col": 0}
            ]

        self.enable_telem_grid = ToggleGrid(enable_telem_info)
        
        toggle_data = [
                {"name": "Front tag detected", "value": False, "able_to_toggle": False, "row": 0, "col": 0},
                {"name": "Back tag detected", "value": False, "able_to_toggle": False, "row": 0, "col": 1}
            ]

        self.toggle_grid = ToggleGrid(toggle_data)
        
        telem_data = [
                {"name": "Front x-pos", "value": "0.00", "row": 0, "col": 0},
                {"name": "Front y-pos", "value": "0.00", "row": 0, "col": 1},
                {"name": "Front timestamp", "value": "0.00", "row": 0, "col": 2},
                {"name": "Back x-pos", "value": "0.00", "row": 1, "col": 0},
                {"name": "Back y-pos", "value": "0.00", "row": 1, "col": 1},
                {"name": "Back timestamp", "value": "0.00", "row": 1, "col": 2}
            ]

        self.telem_grid = TelemGrid(telem_data)
        
        self.drivercam1 = CameraWidget('Driver camera 1')
        self.drivercam2 = CameraWidget('Driver camera 2')
        self.drivercam3 = CameraWidget('Driver camera 3')
        
        self.stream_layout = QVBoxLayout()
        self.stream_layout.addWidget(self.drivercam1)
        self.stream_layout.addWidget(self.drivercam2)
        self.stream_layout.addWidget(self.drivercam3)
        
        self.input_layout = QVBoxLayout()
        self.input_layout.addWidget(self.telem_grid)
        self.input_layout.addWidget(self.toggle_grid)
        self.input_layout.addWidget(self.enable_telem_grid)
        
        self.layout = QHBoxLayout()
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.stream_layout)
        
        self.setLayout(self.layout)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)

    action_grid = VisionDebugWidget()
    action_grid.setWindowTitle("Vision Debugging Window")
    action_grid.resize(600, 400)
    action_grid.show()
    
    sys.exit(app.exec())