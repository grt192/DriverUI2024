from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
from DoubleCam.Widgets.MapDisplayWidget import MapDisplayWidget
from DoubleCam.Widgets.SendIntTupleWidget import SendIntTupleWidget
from DoubleCam.Widgets.SendIncreaseIntWidget import SendIncreaseIntWidget
class MapWidget(QWidget):
    def __init__(self, alliance, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.alignLayout = QVBoxLayout()
        self.sourceAlignWidget = SendIncreaseIntWidget(
            "Source", "Alignment", "Source", self
        )
        self.sourceAlignWidget.setMaximumWidth(115)
        self.alignLayout.addWidget(self.sourceAlignWidget)
        self.ampAlignWidget = SendIncreaseIntWidget(
            "AMP", "Alignment", "AMP", self
        )
        self.ampAlignWidget.setMaximumWidth(115)
        self.alignLayout.addWidget(self.ampAlignWidget)
        self.speakerAlignWidget = SendIncreaseIntWidget(
            "Speaker", "Alignment", "Speaker", self
        )
        self.speakerAlignWidget.setMaximumWidth(115)
        self.alignLayout.addWidget(self.speakerAlignWidget)
        self.layout.addLayout(self.alignLayout)

        self.mapDisplayWidget = MapDisplayWidget(alliance)
        self.mapDisplayWidget.setMaximumWidth(536)
        self.layout.addWidget(self.mapDisplayWidget)

        self.sendDestinationWidget = SendIntTupleWidget("Send Destination", "Map", "TargetX", "Map", "TargetY")
        self.sendDestinationWidget.setMaximumWidth(100)
        self.layout.addWidget(self.sendDestinationWidget)

        self.mapDisplayWidget.newCrosshairPosition.connect(self.sendDestinationWidget.updateMessage)



        self.setLayout(self.layout)

    def changeAllianceColor(self, newAllianceColor:str):
        self.mapDisplayWidget.changeAllianceColor(newAllianceColor)