from networktables import NetworkTables
from PySide6.QtCore import Signal, QObject
import requests
class NestedNetworkTableManager(QObject):
    new_value_available = Signal(str, object)

    #nt debug
    cnt = 0
    def __init__(self, rootTableName, nestedTableNames: list, entryName=""):
        super().__init__()
        NetworkTables.initialize(server='10.1.92.2')

        self.parentTable = NetworkTables.getTable(rootTableName)
        for tableName in nestedTableNames:
            self.nestedTable = self.parentTable.getSubTable(tableName)
            self.parentTable = self.nestedTable
        self.entry_name = entryName
        
        self.nestedTable.addEntryListener(self.valueChanged)

    def valueChanged(self, table, key, value, isNew):
        self.new_value_available.emit(key, value)

    def check_network(self):
        # Check if network is available
        try:
            response = requests.get("http://10.1.92.2:1181", timeout=2)
            return True
        except requests.ConnectionError:
            return False

    def putString(self, message: str):
        print("puting: " + message)
        if (type(message) is not str):
            raise Exception("Wrong message type!")
        self.nestedTable.putString(self.entry_name, str(message))
        #cnt is just for debug
        self.cnt += 1

    def putBool(self, message: bool):
        print("puting: " + str(message) + "\nCurrent table: " + self.tableName + " entry: " + self.entry_name)
        if(type(message) is not bool):
            raise Exception("Wrong message type!")
        self.nestedTable.putBoolean(self.entry_name, message)
        print("finished")
    def putInt(self, message: int):
        if(type(message) is not int):
            raise Exception("Wrong message type!")
        self.nestedTable.putNumber(self.entry_name, message)