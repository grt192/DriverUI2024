from PySide6.QtCore import Signal, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QPushButton
from Widgets.CustomWidgets.BaseWidgets.GradientWarningDoubleDisplayLabel import GradientWarningDoubleDisplayLabel
from Widgets.CustomWidgets.MotorWidget import MotorWidget

class InfoWidget2(QWidget):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.timer = QTimer()
        self.timer.start(500)
        self.climb20Label = MotorWidget("Climb20", "C-Left", self.timer, self)
        self.climb9Label = MotorWidget("Climb9", "C-Right", self.timer, self)
        self.elevator10Label = MotorWidget("Elevator10", "E10", self.timer, self)
        self.elevator11Label = MotorWidget("Elevator11", "E11", self.timer, self)
        self.intake16Label = MotorWidget("Intake16", "I-Pivot", self.timer, self)
        self.intake17Label = MotorWidget("Intake17", "I-Front", self.timer, self)
        self.intake19Label = MotorWidget("Intake19", "Integration", self.timer, self)
        self.shooter12Label = MotorWidget("Shooter12", "S-Pivot", self.timer, self)
        self.shooter13Label = MotorWidget("Shooter13", "S-Top", self.timer, self)
        self.shooter14Label = MotorWidget("Shooter14", "S-Bottom", self.timer, self)
        # self.climb9CurrentLabel = GradientWarningDoubleDisplayLabel(
        #     "CL 9 Current", "Motors", "Climb9Current",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.climb9TemperatureLabel = GradientWarningDoubleDisplayLabel(
        #     "CL 9 Temp", "Motors", "Climb9Temperature",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.climb9VoltageLabel = GradientWarningDoubleDisplayLabel(
        #     "CL 9 Voltage", "Motors", "Climb9Voltage",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.climb20CurrentLabel = GradientWarningDoubleDisplayLabel(
        #     "CL 20 Current", "Motors", "Climb20Current",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.climb20TemperatureLabel = GradientWarningDoubleDisplayLabel(
        #     "CL 20 Temp", "Motors", "Climb20Temperature",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.climb20VoltageLabel = GradientWarningDoubleDisplayLabel(
        #     "CL 20 Voltage", "Motors", "Climb20Voltage",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.elevator10CurrentLabel = GradientWarningDoubleDisplayLabel(
        #     "EL 10 Current", "Motors", "Elevator10Current",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.elevator10VoltageLabel = GradientWarningDoubleDisplayLabel(
        #     "EL 10 Voltage: ", "Motors", "Elevator10Voltage",
        #     (0, 180, 70), (1, 181, 71),
        #     12, 13,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        #
        # self.elevator10TemperatureLabel = GradientWarningDoubleDisplayLabel(
        #     "EL 10 Temp", "Motors", "Elevator10Temperature",
        #     (153, 215, 189), (243, 95, 0),
        #     10, 50,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.elevator11CurrentLabel = GradientWarningDoubleDisplayLabel(
        #     "EL 11 Current", "Motors", "Elevator11Current",
        #     (0, 180, 70), (1, 181, 71),
        #     0, 40,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.elevator11VoltageLabel = GradientWarningDoubleDisplayLabel(
        #     "EL 11 Voltage: ", "Motors", "Elevator11Voltage",
        #     (0, 180, 70), (1, 181, 71),
        #     12, 13,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        # self.elevator11TemperatureLabel = GradientWarningDoubleDisplayLabel(
        #     "EL 11 Temp", "Motors", "Elevator11Temperature",
        #     (153, 215, 189), (243, 95, 0),
        #     10, 50,
        #     self.timer,
        #     "color: white; font-weight: bold; font-size: 15px;",
        #     parent=self, debug=False
        # )
        self.updateButton = QPushButton("Update")
        self.updateButton.setStyleSheet("color: white; font-weight: bold; font-size: 15px;")
        self.updateButton.clicked.connect(self.updateLabels)
        layout = QVBoxLayout(self)
        layout.addWidget(self.climb9Label)
        layout.addWidget(self.climb20Label)
        layout.addWidget(self.elevator10Label)
        layout.addWidget(self.elevator11Label)
        layout.addWidget(self.intake16Label)
        layout.addWidget(self.intake17Label)
        layout.addWidget(self.intake19Label)
        layout.addWidget(self.shooter12Label)
        layout.addWidget(self.shooter13Label)
        layout.addWidget(self.shooter14Label)
        # layout.addWidget(self.climb9CurrentLabel)
        # layout.addWidget(self.climb9TemperatureLabel)
        # layout.addWidget(self.climb9VoltageLabel)
        # layout.addWidget(self.climb20CurrentLabel)
        # layout.addWidget(self.climb20TemperatureLabel)
        # layout.addWidget(self.climb20VoltageLabel)
        # layout.addWidget(self.elevator10CurrentLabel)
        # layout.addWidget(self.elevator10VoltageLabel)
        # layout.addWidget(self.elevator10TemperatureLabel)
        # layout.addWidget(self.elevator11CurrentLabel)
        # layout.addWidget(self.elevator11VoltageLabel)
        # layout.addWidget(self.elevator11TemperatureLabel)
        layout.addWidget(self.updateButton)


    def updateLabels(self):
        self.climb20Label.updateLabels()
        self.climb9Label.updateLabels()
        self.elevator10Label.updateLabels()
        self.elevator11Label.updateLabels()
        # self.elevator10CurrentLabel.manualUpdate()
        # self.elevator10VoltageLabel.manualUpdate()
        # self.elevator10TemperatureLabel.manualUpdate()
        # self.elevator11CurrentLabel.manualUpdate()
        # self.elevator11VoltageLabel.manualUpdate()
        # self.elevator11TemperatureLabel.manualUpdate()