from networktables import NetworkTables
from PySide6.QtCore import Signal, QObject
import requests
class NetworkTableManager(QObject):
    new_value_available = Signal(tuple)
    def __init__(self, tableName, entryName, parent = None):
        super().__init__(parent)
        NetworkTables.initialize(server='10.1.92.2')

        #print("creating table: "+ table_name)
        self.tableName = tableName
        self.table = NetworkTables.getTable(tableName)
        self.entry_name = entryName
        
        self.table.addEntryListener(self.valueChanged)

    def valueChanged(self, table, key, value, isNew):
        if key == self.entry_name:
            self.new_value_available.emit((key, value))

