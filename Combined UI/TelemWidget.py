from PySide6.QtWidgets import QLabel, QVBoxLayout, QGroupBox, QWidget
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtCore import Qt, QTimer
import random

class TelemWidget(QWidget):
    def __init__(self, label, initial_value="N/A", parent=None):
        super().__init__(parent)

        # Set up widgets
        self.group_box = QGroupBox(self)
        self.label = QLabel(label, self.group_box)
        self.value_label = QLabel(str(initial_value), self.group_box)

        # Set up layout
        self.layout = QVBoxLayout(self.group_box)
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the label
        self.layout.addWidget(self.value_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the value label

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.group_box)

        # Adjust font size based on available space
        self.adjust_font_size()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_value)
        self.timer.start(0)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)

    def adjust_font_size(self):
        # Calculate the font size based on available space
        font_metrics = QFontMetrics(self.value_label.font())
        available_width = self.value_label.width()
        text = self.value_label.text()

        # Decrease font size until the text fits within the available width
        font = self.value_label.font()
        while font_metrics.boundingRect(text).width() > available_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)

        # Set the adjusted font size
        self.value_label.setFont(font)

    def set_value(self, value):
        # Set the telemetry value and update the display
        self.value_label.setText(str(value))
        # self.adjust_font_size()
        # "2"

    def update_value(self):
        # IMPLEMENT
        self.set_value(random.randint(1,5))
        self.timer.start(0)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)
        "Run"
