from networktables import NetworkTables
class networktableHelper:
    NetworkTables.initialize(server='127.0.0.1')
    def __init__(self, delegate):
        rollerTable = NetworkTables.getTable("Testing")
        self.delegate = delegate

        rollerTable.addEntryListener(self.valueChanged)

        #self.delegate.xChange(20)
        #self.delegate.yChange(200)
        #self.delegate.zChange(90)

    def valueChanged(self, table, key, value, isNew):
        value = float(value)
        try:
            if key == 'module1vel':
                self.delegate.v1(value)
            elif key == 'module2vel':
                self.delegate.v2(value)
            elif key == 'module3vel':
                self.delegate.v3(value)
            elif key == 'module4vel':
                self.delegate.v4(value)
            elif key == 'module1rot':
                self.delegate.r1(value)
            elif key == 'module2rot':
                self.delegate.r2(value)
            elif key == 'module3rot':
                self.delegate.r3(value)
            elif key == 'module4rot':
                self.delegate.r4(value)
        except Exception as e:
            print(e)