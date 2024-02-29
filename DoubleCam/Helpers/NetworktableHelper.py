from networktables import NetworkTables
from PySide6.QtCore import Signal, QObject
import requests
class NetworkTableManager(QObject):
    new_value_available = Signal(tuple)

    #nt debug
    cnt = 0
    def __init__(self, table_name, entry_name="") -> None:
        super().__init__()
        NetworkTables.initialize(server='10.1.92.2')

        #print("creating table: "+ table_name)
        self.tableName = table_name
        self.table = NetworkTables.getTable(table_name)
        self.entry_name = entry_name
        
        self.table.addEntryListener(self.valueChanged)

    def valueChanged(self, table, key, value, isNew):
        print("Key: " + key + " Value: " + str(value))
        if key == self.entry_name:
            self.new_value_available.emit((key, value))

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
        self.table.putString(self.entry_name, str(message))
        #cnt is just for debug
        self.cnt += 1

    def putBool(self, message: bool):
        print("puting: " + str(message) + "\nCurrent table: " + self.tableName + " entry: " + self.entry_name)
        if(type(message) is not bool):
            raise Exception("Wrong message type!")
        self.table.putBoolean(self.entry_name, message)
        print("finished")
    def putInt(self, message: int):
        if(type(message) is not int):
            raise Exception("Wrong message type!")
        self.table.putNumber(self.entry_name, message)


        
        
        