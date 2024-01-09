import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer

class DriverCamWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Create an ImageItem for displaying the image
        self.image_item = pg.ImageItem()
        self.view_box = pg.ViewBox()
        self.view_box.addItem(self.image_item)

        # Set up the plot widget with the fixed viewbox
        self.plot_widget = pg.PlotWidget(viewBox=self.view_box, enableMenu=False)
        self.layout.addWidget(self.plot_widget)

        # Set the aspect ratio to be equal
        self.plot_widget.setAspectLocked(True)

        # Set the initial image (for visualization purposes)
        self.update_image()

        # Set up a QTimer for constant updates (every 100 milliseconds in this example)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetch_data)
        self.timer.start(100)

    def update_image(self):
        # Generate random image data (replace this with your actual data)
        image_data = np.random.randint(0, 256, size=(160, 320), dtype=np.uint8)

        # Update the ImageItem with the new image data
        self.image_item.setImage(image_data, autoLevels=True, autoDownsample=True)

    def fetch_data(self):
        # Fetch new data and update the image
        self.update_image()

# Example usage
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication

    app = QApplication([])

    window = DriverCamWidget()
    window.show()

    app.exec()
