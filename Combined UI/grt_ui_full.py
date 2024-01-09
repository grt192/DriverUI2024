import os
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from networktableHelper import networktableHelper
from mapLabel import mapLabel

from ControlPanel import ControlPanel
from driver_cam.DriverCameraWidget import CameraWidget
from MapWidget import GRTMapWidget
from TelemGrid import TelemGrid
from ToggleGrid import ToggleGrid

class GRTDriverStation(QMainWindow):
    QCheckBoxWidth = 50
    QCheckBoxHeight = 50

    def __init__(self):
        super().__init__()

        self.alliance = 'red'

        # Set up the main window
        self.setWindowTitle("GRT 192 Driver Station")
        self.resize(1920, 1080)
        # Create a central widget and set a layout for it
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout() # MAIN LAYOUT HAS THE PREMATCH CONTROL PANEL + THE REST OF THE UI
        self.central_widget.setLayout(self.main_layout)

        #Control Panel
        self.control_panel = ControlPanel(self.alliance, self) # CONTROL PANEL IS USED FOR PRE MATCH SETTINGS
        # Create a QVBoxLayout to organize the widgets
        self.match_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.control_panel)
        self.main_layout.addLayout(self.match_layout)

        # Create the tab widget
        self.match_debug_tab_widget = QTabWidget(self.central_widget)

        # Create and add tabs
        self.match_tab = QWidget()
        self.debug_tab = QWidget()

        self.match_debug_tab_widget.addTab(self.match_tab, "Match")
        self.match_debug_tab_widget.addTab(self.debug_tab, "Debug")

        self.match_layout.addWidget(self.match_debug_tab_widget)

        self.map_widget = GRTMapWidget(self.alliance)
        self.driver_cam = CameraWidget()
        
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
                {"name": "Toggle 1", "value": True},
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
        self.match_telem_layout.addWidget(self.driver_cam)
        self.match_telem_layout.addLayout(self.telem_toggle_layout)

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

        self.clickXDisplay = QLabel(self.match_tab)
        self.clickXDisplay.setGeometry(1880, 50, 20, 10)

        self.clickYDisplay = QLabel(self.match_tab)
        self.clickYDisplay.setGeometry(1880, 65, 20, 10)

        self.visionSwitch = QCheckBox(self.match_tab)
        self.visionSwitch.setGeometry(QRect(1850, 80, self.QCheckBoxWidth, self.QCheckBoxHeight))

        # Create a QHBoxLayout for the row of buttons
        button_layout = QHBoxLayout()

        # Create buttons and set their icons as backgrounds
        self.amp_button = QPushButton(self.match_tab)
        self.amp_button.setIcon(QIcon(f"{os.path.dirname(__file__)}/ui_images/{self.alliance}_amp.png"))
        self.amp_button.setStyleSheet("border: none;")
        self.amp_button.setFixedSize(150, 150)  # Set the size of the button
        self.amp_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fix the size policy
        self.amp_button.setIconSize(QSize(150, 150))  # Set the size of the icon

        self.source_button = QPushButton(self.match_tab)
        self.source_button.setIcon(QPixmap(f"{os.path.dirname(__file__)}/ui_images/{self.alliance}_source.png"))
        self.source_button.setStyleSheet("border: none;")
        self.source_button.setFixedSize(150, 150)  # Set the size of the button
        self.source_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fix the size policy
        self.source_button.setIconSize(QSize(150, 150))  # Set the size of the icon

        self.speaker_button = QPushButton(self.match_tab)
        self.speaker_button.setIcon(QIcon(f"{os.path.dirname(__file__)}/ui_images/{self.alliance}_speaker.png"))
        self.speaker_button.setStyleSheet("border: none;")
        self.speaker_button.setFixedSize(150, 150)  # Set the size of the button
        self.speaker_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Fix the size policy
        self.speaker_button.setIconSize(QSize(150, 150))  # Set the size of the icon

        # Add your buttons to the button_layout
        button_layout.addWidget(self.amp_button)
        button_layout.addWidget(self.source_button)
        button_layout.addWidget(self.speaker_button)

        # Add the button_layout to the main layout
        self.match_layout.addLayout(button_layout)

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
