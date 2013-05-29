class Testboard:
    def __init__(self,slot,module,address,type):
        self.slot=slot
        self.module=module
        self.address=address
        self.type=type
        self.tests=[]
        self.currenttest=''
        self.testdir=''
        self.defparamdir=''
        self.powerdup=False
        self.busy=False
        self.timestamp=0
        self.active=True
        self.numerator = 0
        self.dataDir ='.'
        self.moduleDir ='MXXXX'
    @property
    def parentDir(self):
        return '%s/%s/'%(self.dataDir,self.moduleDir)