from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from DoubleCam.Widgets.MapDisplayWidget import MapDisplayWidget
from DoubleCam.Widgets.SendIntTupleWidget import SendIntTupleWidget

class MapWidget(QWidget):
    def __init__(self, alliance, parent=None):
        super().__init__(parent)

        self.mapDisplayWidget = MapDisplayWidget(alliance)
        self.mapDisplayWidget.setMaximumWidth(536)
        self.sendDestinationWidget = SendIntTupleWidget("Send Destination", "Map", "TargetX", "Map", "TargetY")
        self.sendDestinationWidget.setMaximumWidth(100)

        self.mapDisplayWidget.newCrosshairPosition.connect(self.sendDestinationWidget.updateMessage)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.mapDisplayWidget)
        self.layout.addWidget(self.sendDestinationWidget)
        self.setLayout(self.layout)

    def changeAllianceColor(self, newAllianceColor:str):
        self.mapDisplayWidget.changeAllianceColor(newAllianceColor)