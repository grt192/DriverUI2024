import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from networktableHelper import networktableHelper
from NetworktableHelper2 import NetworkTableManager
from mapLabel import mapLabel
from MapWidget import MapWidget
from ControlPanel import ControlPanel
from DriverCameraWidget import CameraWidget
from TelemGrid import TelemGrid
from ToggleGrid import ToggleGrid
from ActionGrid import ActionGrid
from SwerveWheelWidget import SwerveWheelWidget
from vision_debug_ui import VisionDebugWidget

class GRTDriverStation(QMainWindow):
    QCheckBoxWidth = 50
    QCheckBoxHeight = 50

    def __init__(self):
        super().__init__()

        self.alliance = 'red'

        self.setWindowTitle("GRT 192 Driver Station")
        self.resize(1920, 1080)

        # MAIN LAYOUT HAS THE PREMATCH CONTROL PANEL + THE REST OF THE UI
        self.mainLayout = QHBoxLayout()

        # Set the UI's central widget to a widget, and set that widget's layout to the whole UI
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.mainLayout)

        # The control panel is used for holistic settings across the UI (e.g. alliance color, auton selection)
        # NOT meant for mid-match inputs
        self.controlPanel = ControlPanel()

        # The content layout is for the primary content of the GUI.
        self.contentLayout = QVBoxLayout()

        # Adding widgets and layouts to the main layout
        # Since it's a horizontal layout, we're adding elements in order of left to right
        # The control panel goes on the left, followed by the content layout with everything else
        self.mainLayout.addWidget(self.controlPanel)
        self.mainLayout.addLayout(self.contentLayout)

        ''' 
        Everything that's not the control panel will end up in one of four (?) tabs:
            1. Auton - Visualizing the autonomous paths, possibly plotting and/or tuning?
            2. Match - Telemetry and visualizations, driver inputs (MOST IMPORTANT)
            3. Debug - Testing/Fixing stuff in the pits (e.g. testing swerve, simulating auton)
            4. Vision - Testing/Fixing vision (apriltags + driver cams) in the pits (e.g. 'are tags detected?')
        
        '''

        self.match_debug_tab_widget = QTabWidget(self.centralWidget)

        # Create and add the tabs as three widgets
        self.autonTab = QWidget()
        self.matchTab = QWidget()
        self.debugTab = QWidget()
        self.visionTab = QWidget()

        #Added tabs to the tab widget
        self.match_debug_tab_widget.addTab(self.autonTab, "Auton")
        self.match_debug_tab_widget.addTab(self.matchTab, "Match")
        self.match_debug_tab_widget.addTab(self.debugTab, "Debug")
        self.match_debug_tab_widget.addTab(self.visionTab, "Vision")

        self.match_debug_tab_widget.setCurrentIndex(1)

        # The tabs are really the only thing in the content layout
        self.contentLayout.addWidget(self.match_debug_tab_widget)

        self.map_widget = MapWidget(self.alliance)
        
        self.cameraAndActionLayout = QVBoxLayout()
        self.driverCameraWidget = CameraWidget()

        # Define a list of dictionaries with ActionWidget parameters
        """
        actions_info = [
            {"action_name": "GO TO AMP", "alliance": self.alliance, "table_name": "PhotonVision", "entry_name": "xPosFront", "row": 0, "col": 0},
            {"action_name": "GO TO SPEAKER", "alliance": self.alliance, "table_name": "PhotonVision", "entry_name": "xPosFront", "row": 0, "col": 1},
            {"action_name": "GO TO SOURCE", "alliance": self.alliance, "table_name": "PhotonVision", "entry_name": "xPosFront", "row": 0, "col": 2},
            {"action_name": "SCORE AMP", "alliance": self.alliance, "table_name": "PhotonVision", "entry_name": "xPosFront", "row": 1, "col": 0},
            {"action_name": "SCORE SPEAKER", "alliance": self.alliance, "table_name": "PhotonVision", "entry_name": "xPosFront", "row": 1, "col": 1},
            {"action_name": "INTAKE SOURCE", "alliance": self.alliance, "table_name": "PhotonVision", "entry_name": "xPosFront", "row": 1, "col": 2},
        ]
        """

        """
        actions_info = [
            {"action_name": "GO TO AMP", "alliance": self.alliance, "row": 0, "col": 0, "table_name": "elevator", "entry_name": "target_location"},
            {"action_name": "GO TO SPEAKER", "alliance": self.alliance, "row": 0, "col": 1, "table_name": "elevator", "entry_name": "target_location"},
            {"action_name": "GO TO SOURCE", "alliance": self.alliance, "row": 0, "col": 2, "table_name": "elevator", "entry_name": "target_location"},
            {"action_name": "SCORE AMP", "alliance": self.alliance, "row": 0, "col": 2, "table_name": "elevator", "entry_name": "target_location"},
            {"action_name": "SCORE SPEAKER", "alliance": self.alliance, "row": 0, "col": 2, "table_name": "elevator", "entry_name": "target_location"},
            {"action_name": "INTAKE SOURCE", "alliance": self.alliance, "row": 0, "col": 2, "table_name": "elevator", "entry_name": "target_location"},
        ]
        """
        actions_info = [
            {"action_name": "Go TO AMP", "alliance": self.alliance, "row": 0, "col": 0,
             "table_name": "", "entry_name": ""},
            {"action_name": "GO TO SPEAKER", "alliance": self.alliance, "row": 0, "col": 1,
             "table_name": "", "entry_name": "", "message": ""},
            {"action_name": "GO TO SOURCE", "alliance": self.alliance, "row": 0, "col": 2,
             "table_name": "", "entry_name": "", "message": ""},
            {"action_name": "Go TO AMP", "alliance": self.alliance, "row": 1, "col": 0,
             "table_name": "elevator", "entry_name": "target_position", "message": "AMP"},
            {"action_name": "SCORE SPEAKER", "alliance": self.alliance, "row": 1, "col": 1,
             "table_name": "elevator", "entry_name": "target_position", "message": "SPEAKER"},
            {"action_name": "INTAKE SOURCE", "alliance": self.alliance, "row": 1, "col": 2,
             "table_name": "elevator", "entry_name": "target_position", "message": "GROUND"},
        ]
        self.actionGrid = ActionGrid(actions_info)
        self.controlPanel.alliance_color_changed.connect(self.actionGrid.change_alliance_color)
        self.controlPanel.alliance_color_changed.connect(self.map_widget.change_alliance_color)
        
        self.cameraAndActionLayout.addWidget(self.driverCameraWidget)
        self.cameraAndActionLayout.addWidget(self.actionGrid)


        self.telem_toggle_layout = QVBoxLayout()
        
        self.telem_widget_data_preset = [
                {"name": "Front x-pos", "value": "0.00", "table_name": "PhotonVision", "entry_name": "xPosFront", "row": 0, "col": 0},
                {"name": "Front y-pos", "value": "0.00", "table_name": "PhotonVision", "entry_name": "yPosFront", "row": 0, "col": 1},
                {"name": "Front Heading", "value": "0.00", "table_name": "PhotonVision", "entry_name": "headingFront", "row": 0, "col": 2},
                {"name": "Back x-pos", "value": "0.00", "table_name": "PhotonVision", "entry_name": "xPosBack", "row": 1, "col": 0},
                {"name": "Back y-pos", "value": "0.00", "table_name": "PhotonVision", "entry_name": "yPosBack", "row": 1, "col": 1},
                {"name": "Back Heading", "value": "0.00", "table_name": "PhotonVision", "entry_name": "headingBack", "row": 1, "col": 2}
                # {"name": "Quantity", "value": "0.00", "table_name": "PhotonVision", "entry_name": "headingBack","row": 2, "col": 0},
                # {"name": "Quantity", "value": "0.00", "table_name": "PhotonVision", "entry_name": "headingBack", "row": 2, "col": 1},
                # {"name": "Quantity", "value": "0.00", "table_name": "PhotonVision", "entry_name": "headingBack", "row": 2, "col": 2}
        ]

        self.telem_grid = TelemGrid(self.telem_widget_data_preset)
        
        self.toggle_widget_data_preset = [
                {"name": "Vision", "value": True , "states": ('Enabled', 'Disabled'), "colors": ('green', 'red'), "row": 0, "col": 0},
                {"name": "Relative to", "value": True , "states": ('Field ', 'Robot'), "colors": ('green', 'red'), "row": 0, "col": 1},
                {"name": "Toggle 3", "value": True, "row": 0, "col": 2},
                {"name": "Toggle 4", "value": False, "row": 1, "col": 0},
                {"name": "Toggle 5", "value": True, "row": 1, "col": 1},
                {"name": "Toggle 6", "value": False, "row": 1, "col": 2},
                {"name": "Toggle 7", "value": True, "row": 2, "col": 0},
                {"name": "Toggle 8", "value": False, "row": 2, "col": 1},
                {"name": "Toggle 9", "value": True, "row": 2, "col": 2},
            ]

        self.toggle_grid = ToggleGrid(self.toggle_widget_data_preset)
        
        self.telem_toggle_layout.addWidget(self.telem_grid)
        self.telem_toggle_layout.addWidget(self.toggle_grid)
        
        self.matchAndTelemetryLayout = QHBoxLayout(self.matchTab)
        #Add mapWidget, cameraAndActionLayout, and telem_toggle_layout to match tab.
        self.matchAndTelemetryLayout.addWidget(self.map_widget)
        self.matchAndTelemetryLayout.addLayout(self.cameraAndActionLayout)
        self.matchAndTelemetryLayout.addLayout(self.telem_toggle_layout)

        self.swerve_debug_layout = QHBoxLayout(self.debugTab)
        self.swerve_wheel_model = SwerveWheelWidget()
        self.swerve_auton_map_model = MapWidget(self.alliance)
        self.swerve_debug_layout.addWidget(self.swerve_wheel_model)
        self.swerve_debug_layout.addWidget(self.swerve_auton_map_model)
        
        self.vision_debug_layout = QHBoxLayout(self.visionTab)
        self.vision_debug_widget = VisionDebugWidget()
        self.vision_debug_layout.addWidget(self.vision_debug_widget)
        
        # Add content to Tab 1
        # crosshair.png is 30*30
        self.crosshair1 = QLabel(self.matchTab)
        self.crosshair1.setObjectName("crosshair1")
        self.crosshair1.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.crosshair1.setPixmap(QPixmap(f"{os.path.dirname(__file__)}/crosshair.png"))
        self.crosshair1.hide()

        self.robot = QLabel(self.matchTab)
        self.robot.setObjectName("robot")
        self.robotPixmap = QPixmap(f"{os.path.dirname(__file__)}/RobotArrow.png")
        self.robot.setPixmap(self.robotPixmap)
        self.robot.setGeometry(QtCore.QRect(15, 15, 30, 30))
        self.robot.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.robot.hide()

        rotation_angle = 90 if self.alliance == "red" else -90  # Choose the rotation angle based on the alliance
        
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
    sdf = NetworkTableManager(table_name="df", entry_name="clean_GRT_UI")
    main()
