from networktables import NetworkTables
class networktableHelper:
    NetworkTables.initialize(server='10.1.92.2')
    def __init__(self, delegate):
        rollerTable = NetworkTables.getTable("Roller")
        rValue = rollerTable.getAutoUpdateValue("R",0)
        gValue = rollerTable.getAutoUpdateValue("G",0)
        bValue = rollerTable.getAutoUpdateValue('B',0)
        self.delegate = delegate

        rollerTable.addEntryListener(self.valueChanged)
    @staticmethod
    def valueChanged(self, key, value, isNew):
        if not isNew:
            return
        if key == 'R':
            self.delegate.rChanged(value)
        elif key == 'G':
            self.delegate.gChanged(value)
        elif key == 'B':
            self.delegate.bChanged(value)