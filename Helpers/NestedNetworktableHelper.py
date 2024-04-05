from networktables import NetworkTables
from PySide6.QtCore import Signal, QObject
import requests
class NestedNetworkTableManager(QObject):
    new_value_available = Signal(tuple)
    def __init__(self, tableNames: list, entryName: str):
        super().__init__()
        NetworkTables.initialize(server='10.1.92.2')

        self.table = NetworkTables.getTable(tableNames[0])
        for i in range (1, len(tableNames)):
            self.table = self.table.getSubTable(tableNames[i])
        self.entry_name = entryName
        
        self.table.addEntryListener(self.valueChanged)
        self.entry = self.table.getEntry(self.entry_name)
        self.entry.addListener(self.valueChanged, NetworkTables.NotifyFlags.UPDATE)

    def valueChanged(self, table, key, value, isNew):
        self.new_value_available.emit((key, value))

    def getValue(self):
        return self.table.getValue(self.entry_name, 0)