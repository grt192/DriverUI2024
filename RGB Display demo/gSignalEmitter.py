from PyQt5.QtCore import QObject, pyqtSignal
class gSignalEmitter(QObject):
    gSignal = pyqtSignal(str)