from networktables import NetworkTables
class networktableHelper:
    NetworkTables.initialize(server='10.1.92.2')
    def __init__(self, delegate):
        rollerTable = NetworkTables.getTable("Testing")
        self.delegate = delegate

        rollerTable.addEntryListener(self.valueChanged)
    def valueChanged(self, table, key, value, isNew):
        value = str(value)
        if not isNew:
            return
        if key == 'R':
            self.delegate.rChange(value)
        """
        elif key == 'G':
            self.delegate.gChange(value)
        elif key == 'B':
            self.delegate.bChange(value)
            """