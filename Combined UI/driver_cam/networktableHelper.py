from networktables import NetworkTables
class networktableHelper:
    NetworkTables.initialize(server='10.1.92.2')
    def __init__(self, delegate):
        rollerTable = NetworkTables.getTable("Testing")
        self.delegate = delegate

        rollerTable.addEntryListener(self.valueChanged)

        #self.delegate.xChange(20)
        #self.delegate.yChange(200)
        #self.delegate.zChange(90)

    def valueChanged(self, table, key, value, isNew):
        value = str(value)
        try:
            if key == 'x':
                #print("x: "+str(value))
                self.delegate.xChange(float(value))
            elif key == 'y':
                #print("y: "+str(value))
                self.delegate.yChange(float(value))
            elif key == 'z':
                #print("z: "+str(value))
                self.delegate.zChange(float(value))
        except Exception as e:
            print(e)