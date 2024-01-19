from networktables import NetworkTables
from PySide6.QtCore import Qt, Signal, QObject, Slot
import requests

class NetworkTableManager(QObject):
    new_value_available = Signal(str, object)
    
    def __init__(self, table_name, entry_name="") -> None:
        super().__init__()
        NetworkTables.initialize(server='10.1.92.2')

        print("creating table: "+ table_name)
        self.table = NetworkTables.getTable(table_name)
        self.entry_name = entry_name
        
        self.table.addEntryListener(self.valueChanged)

    def valueChanged(self, table, key, value, isNew):

        # if key == self.entry_name:
        #     self.new_value_available.emit(key, value)
        
        self.new_value_available.emit(key, value)
        
        # try:
        #     if key == 'x':
        #         #print("x: "+str(value))
        #         self.delegate.xChange(float(value))
        #     elif key == 'y':
        #         #print("y: "+str(value))
        #         self.delegate.yChange(float(value))
        #     elif key == 'z':
        #         #print("z: "+str(value))
        #         self.delegate.zChange(float(value))
        # except Exception as e:
        #     print(e)
        
    def check_network(self):
        # Check if network is available
        try:
            response = requests.get("http://10.1.92.2:1181", timeout=2)
            return True
        except requests.ConnectionError:
            return False

    def putString(self, message):
        print("puting: " + message)
        self.table.putString(self.entry_name, message)
        print(1)
        
        
        
        