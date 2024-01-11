from PyQt6.QtCore import QObject, pyqtSignal
class gSignalEmitter(QObject):
    gSignal = pyqtSignal(str)