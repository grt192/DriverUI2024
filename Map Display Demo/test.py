from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QMainWindow
from PyQt6.QtGui import QPixmap
import os

class ImageOverlayApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.central_widget = QGraphicsView()
        self.setCentralWidget(self.central_widget)

        # Create a QGraphicsScene
        scene = QGraphicsScene(self)
        self.central_widget.setScene(scene)

        # Load the first image
        image1 = QGraphicsPixmapItem(QPixmap(f'{os.path.dirname(__file__)}/field23.png') )
        scene.addItem(image1)

        # Load the second image
        image2 = QGraphicsPixmapItem(QPixmap(f'{os.path.dirname(__file__)}/grt23robot.png'))
        image2.setPos(50, 50)  # Adjust the position of the second image
        scene.addItem(image2)

if __name__ == '__main__':
    app = QApplication([])
    mainWin = ImageOverlayApp()
    mainWin.show()
    app.exec()
