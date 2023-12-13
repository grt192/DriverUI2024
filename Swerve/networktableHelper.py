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
            if key == 'r1':
                #print("x: "+str(value))
                self.delegate.r1(int(value))
            elif key == 'r2':
                #print("y: "+str(value))
                self.delegate.r2(int(value))
            elif key == 'r3':
                #print("z: "+str(value))
                self.delegate.r3(int(value))
            elif key == 'r4':
                self.delegate.r4(int(value))
            elif key == 'v1':
                self.delegate.v1(int(value))
            elif key == 'v2':
                self.delegate.v2(int(value))
            elif key == 'v3':
                self.delegate.v3(int(value))
            elif key == 'v4':
                self.delegate.v4(int(value))
        except Exception as e:
            print(e)