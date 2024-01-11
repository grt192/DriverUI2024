from PyQt6.QtCore import QObject, pyqtSignal
class rSignalEmitter(QObject):
    rSignal = pyqtSignal(str)