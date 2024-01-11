from PySide6.QtWidgets import QLabel

class mapLabel(QLabel):
    def __init__(self, widget, delegate):
        super().__init__(widget)
        self.delegate = delegate
    def mousePressEvent(self, event):
       self.delegate.getClickPosition(event.pos())
