import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from networktableHelper import networktableHelper
from mapLabel import mapLabel
from MapWidget import MapWidget
from ControlPanel import ControlPanel
from DriverCameraWidget import CameraWidget
from TelemGrid import TelemGrid
from ToggleGrid import ToggleGrid
from ActionGrid import ActionGrid
from SwerveWheelWidget import SwerveWheelWidget

class GRTDriverStation(QMainWindow):
    QCheckBoxWidth = 50
    QCheckBoxHeight = 50

    def __init__(self):
        super().__init__()

        self.alliance = 'red'

        self.setWindowTitle("GRT 192 Driver Station")
        self.resize(1920, 1080)
        
        # MAIN LAYOUT HAS THE PREMATCH CONTROL PANEL + THE REST OF THE UI
        self.main_layout = QHBoxLayout() 
        
        # Set the UI's central widget to a widget, and set that widget's layout to the whole UI
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)
        
        # The control panel is used for holistic settings across the UI (e.g. alliance color, auton selection)
        # NOT meant for mid-match inputs
        self.control_panel = ControlPanel() 
        
        # The content layout is for the primary content of the GUI.
        self.content_layout = QVBoxLayout(self.central_widget)
        
        # Adding widgets and layouts to the main layout
        # Since it's a horizontal layout, we're adding elements in order of left to right
        # The control panel goes on the left, followed by the content layout with everything else
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addLayout(self.content_layout)
        
        ''' 
        Everything that's not the control panel will end up in one of three (?) tabs:
            1. Auton - Visualizing the autonomous paths, possibly plotting and/or tuning?
            2. Match - Telemetry and visualizations, driver inputs (MOST IMPORTANT)
            3. Debug - Testing/Fixing stuff in the pits (e.g. testing swerve, simulating auton)
        
        '''
        self.match_debug_tab_widget = QTabWidget(self.central_widget)

        # Create and add the tabs as three widgets
        self.auton_tab = QWidget()
        self.match_tab = QWidget()
        self.debug_tab = QWidget()

        self.match_debug_tab_widget.addTab(self.auton_tab, "Auton")
        self.match_debug_tab_widget.addTab(self.match_tab, "Match")
        self.match_debug_tab_widget.addTab(self.debug_tab, "Debug")
        self.match_debug_tab_widget.setCurrentIndex(1)

        # The tabs are really the only thing in the content layout
        self.content_layout.addWidget(self.match_debug_tab_widget)

        self.map_widget = MapWidget(self.alliance)
        
        self.cam_action_layout = QVBoxLayout()
        # self.driver_cam = CameraWidget()
        
        # Define a list of dictionaries with ActionWidget parameters
        actions_info = [
            {"action_name": "GO TO AMP", "alliance": self.alliance},
            {"action_name": "GO TO SPEAKER", "alliance": self.alliance},
            {"action_name": "GO TO SOURCE", "alliance": self.alliance},
            {"action_name": "SCORE AMP", "alliance": self.alliance},
            {"action_name": "SCORE SPEAKER", "alliance": self.alliance},
            {"action_name": "INTAKE SOURCE", "alliance": self.alliance},
        ]

        self.action_grid = ActionGrid(actions_info)
        self.control_panel.alliance_color_changed.connect(self.action_grid.change_alliance_color)
        self.control_panel.alliance_color_changed.connect(self.map_widget.change_alliance_color)
        
        # self.cam_action_layout.addWidget(self.driver_cam)
        self.cam_action_layout.addWidget(self.action_grid)
        
        self.telem_toggle_layout = QVBoxLayout()
        
        self.telem_widget_data_preset = [
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"},
                {"name": "Quantity", "value": "0.00"}
            ]

        self.telem_grid = TelemGrid(self.telem_widget_data_preset)
        
        self.toggle_widget_data_preset = [
                {"name": "Vision", "value": True , "states": ('Enabled', 'Disabled'), "colors": ('green', 'red')},
                {"name": "Toggle 2", "value": False},
                {"name": "Toggle 3", "value": True},
                {"name": "Toggle 4", "value": False},
                {"name": "Toggle 5", "value": True},
                {"name": "Toggle 6", "value": False},
                {"name": "Toggle 7", "value": True},
                {"name": "Toggle 8", "value": False},
                {"name": "Toggle 9", "value": True},
            ]

        self.toggle_grid = ToggleGrid(self.toggle_widget_data_preset)
        
        self.telem_toggle_layout.addWidget(self.telem_grid)
        self.telem_toggle_layout.addWidget(self.toggle_grid)
        
        self.match_telem_layout = QHBoxLayout(self.match_tab)
        self.match_telem_layout.addWidget(self.map_widget)
        self.match_telem_layout.addLayout(self.cam_action_layout)
        self.match_telem_layout.addLayout(self.telem_toggle_layout)

        self.swerve_debug_layout = QHBoxLayout(self.debug_tab)
        self.swerve_wheel_model = SwerveWheelWidget()
        self.swerve_auton_map_model = MapWidget(self.alliance)
        self.swerve_debug_layout.addWidget(self.swerve_wheel_model)
        self.swerve_debug_layout.addWidget(self.swerve_auton_map_model)

        # # Add content to Tab 1
        # # crosshair.png is 30*30
        # self.crosshair1 = QLabel(self.match_tab)
        # self.crosshair1.setObjectName("crosshair1")
        # self.crosshair1.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        # self.crosshair1.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/crosshair.png"))
        # self.crosshair1.hide()

        # self.robot = QLabel(self.match_tab)
        # self.robot.setObjectName("robot")
        # self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/RobotArrow.png")
        # self.robot.setPixmap(self.robotPixmap)
        # self.robot.setGeometry(QtCore.QRect(15, 15, 30, 30))
        # self.robot.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        # self.robot.hide()

        # rotation_angle = 90 if self.alliance == "red" else -90  # Choose the rotation angle based on the alliance
        
        # self.field = mapLabel(self.match_tab, self)
        # self.field.setObjectName("field")
        # self.fieldPixmap = QPixmap(f"{os.path.dirname(__file__)}/field24.png").scaled(600, 300)
        # self.field.setPixmap(self.fieldPixmap)
        # self.fieldOffsetX = 20
        # self.fieldOffsetY = 74
        # self.field.setGeometry(QtCore.QRect(self.fieldOffsetX, self.fieldOffsetY, 600, 300))
        
        # transform = QTransform().rotate(rotation_angle)
        # rotated_pixmap = self.fieldPixmap.transformed(transform)

        # self.field.setPixmap(rotated_pixmap)
        '''
        self.clickXDisplay = QLabel(self.match_tab)
        self.clickXDisplay.setGeometry(1880, 50, 20, 10)

        self.clickYDisplay = QLabel(self.match_tab)
        self.clickYDisplay.setGeometry(1880, 65, 20, 10)

        self.visionSwitch = QCheckBox(self.match_tab)
        self.visionSwitch.setGeometry(QRect(1850, 80, self.QCheckBoxWidth, self.QCheckBoxHeight))
        '''
        # # Create a QHBoxLayout for the row of buttons
        # button_layout = QHBoxLayout()

        # # Create buttons and set their icons as backgrounds
        # self.amp_button = QPushButton(self.match_tab)
        # self.amp_button.setIcon(QIcon(f"{os.path.dirname(__file__)}/ui_images/{self.alliance}_amp.png"))
        # self.amp_button.setStyleSheet("border: none;")
        # self.amp_button.setFixedSize(150, 150)  # Set the size of the button
        # self.amp_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fix the size policy
        # self.amp_button.setIconSize(QSize(150, 150))  # Set the size of the icon

        # self.source_button = QPushButton(self.match_tab)
        # self.source_button.setIcon(QPixmap(f"{os.path.dirname(__file__)}/ui_images/{self.alliance}_source.png"))
        # self.source_button.setStyleSheet("border: none;")
        # self.source_button.setFixedSize(150, 150)  # Set the size of the button
        # self.source_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fix the size policy
        # self.source_button.setIconSize(QSize(150, 150))  # Set the size of the icon

        # self.speaker_button = QPushButton(self.match_tab)
        # self.speaker_button.setIcon(QIcon(f"{os.path.dirname(__file__)}/ui_images/{self.alliance}_speaker.png"))
        # self.speaker_button.setStyleSheet("border: none;")
        # self.speaker_button.setFixedSize(150, 150)  # Set the size of the button
        # self.speaker_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fix the size policy
        # self.speaker_button.setIconSize(QSize(150, 150))  # Set the size of the icon

        # # Add your buttons to the button_layout
        # button_layout.addWidget(self.amp_button)
        # button_layout.addWidget(self.source_button)
        # button_layout.addWidget(self.speaker_button)

        # # Add the button_layout to the main layout
        # self.match_layout.addLayout(button_layout)

        # Initialize other components as needed
        self.networktableHelper = networktableHelper(self)

    def getClickPosition(self, pos):
        print(str(pos.x()) + " " + str(pos.y()))
        self.clickXDisplay.setText(str(pos.x()))
        self.clickYDisplay.setText(str(pos.y()))
        self.crosshair1.setGeometry(pos.x() - 9 + self.fieldOffsetX, pos.y() - 9 + self.fieldOffsetY, 20, 20)
        self.crosshair1.show()
        self.crosshair1.raise_()

    def changeAlliance(self, newAlliance):
        self.alliance = newAlliance
        #Refresh widget colors
def main():
    app = QApplication([])
    window = GRTDriverStation()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
