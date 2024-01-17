from PySide6.QtWidgets import QLabel, QVBoxLayout, QGroupBox, QWidget, QSizePolicy
from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtCore import Qt, QTimer, Slot
from NetworktableHelper2 import NetworkTableManager
import random

class TelemWidget(QWidget):
    def __init__(self, label, table_name, entry_name, initial_value="N/A", parent=None):
        super().__init__(parent)

        # Set up widgets
        self.group_box = QGroupBox(self)
        self.label = QLabel(label, self.group_box)
        self.value_label = QLabel(str(initial_value), self.group_box)
        
        self.value_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        
        self.nt_manager = NetworkTableManager(table_name=table_name, entry_name=entry_name)
        self.nt_manager.new_value_available.connect(self.update_nt_value)

        # Set up layout
        self.layout = QVBoxLayout(self.group_box)
        self.layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the label
        self.layout.addWidget(self.value_label, alignment=Qt.AlignmentFlag.AlignCenter)  # Center the value label

        # Set up main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.group_box)

        # Adjust font size based on available space
        # self.adjust_font_size()
        
        self.timer = QTimer()
        # self.timer.timeout.connect(self.update_nt_value)
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
        self.set_value(round(random.randint(1,5)*1.05, 2))
        self.timer.start(0)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)

    @Slot(str, object)
    def update_nt_value(self, key:str, value:object):
        print("trying to nt telem")
        self.set_value(round(value, 2))
        # self.timer.start(0)  # Adjust the interval as needed (e.g., 100 ms for 10 FPS)