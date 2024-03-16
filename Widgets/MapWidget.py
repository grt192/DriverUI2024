from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget
from Widgets.MapDisplayWidget import MapDisplayWidget
from Widgets.SendIntTupleWidget import SendIntTupleWidget
from Widgets.SendIncreaseIntWidget import SendIncreaseIntWidget
class MapWidget(QWidget):
    def __init__(self, alliance, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()
        self.alignLayout = QVBoxLayout()
        self.setContentsMargins(0,0,0,0)
        # self.sourceAlignWidget = SendIncreaseIntWidget(
        #     "Source", "Alignment", "Source", self
        # )
        # self.sourceAlignWidget.setMaximumWidth(115)
        # self.alignLayout.addWidget(self.sourceAlignWidget)
        # self.ampAlignWidget = SendIncreaseIntWidget(
        #     "AMP", "Alignment", "AMP", self
        # )
        # self.ampAlignWidget.setMaximumWidth(115)
        # self.alignLayout.addWidget(self.ampAlignWidget)
        # self.speakerAlignWidget = SendIncreaseIntWidget(
        #     "Speaker", "Alignment", "Speaker", self
        # )
        # self.speakerAlignWidget.setMaximumWidth(115)
        # self.alignLayout.addWidget(self.speakerAlignWidget)
        # self.layout.addLayout(self.alignLayout)

        self.mapDisplayWidget = MapDisplayWidget(alliance)
        self.mapDisplayWidget.setContentsMargins(0,0,0,0)
        self.mapDisplayWidget.setMaximumWidth(400)
        self.mapDisplayWidget.setMaximumHeight(806)
        self.layout.addWidget(self.mapDisplayWidget)

        # self.sendDestinationWidget = SendIntTupleWidget("Send Destination", "Map", "TargetX", "Map", "TargetY")
        # self.sendDestinationWidget.setMaximumWidth(100)
        # self.layout.addWidget(self.sendDestinationWidget)

        # self.mapDisplayWidget.newCrosshairPosition.connect(self.sendDestinationWidget.updateMessage)



        self.setLayout(self.layout)

    def changeAllianceColor(self, newAllianceColor:str):
        self.mapDisplayWidget.changeAllianceColor(newAllianceColor)