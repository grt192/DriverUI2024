from PyQt5.QtCore import QObject, pyqtSignal
class bSignalEmitter(QObject):
    bSignal = pyqtSignal(str)