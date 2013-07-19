## @file
## Defines the class environment.environment
## @ingroup elComandante
## @ingroup elAgente

## Class that contains information about a test environment
##
## This class contains physical parameters of a test environment such
## as temperature and x-ray radiation. Environments can be either defined
## either by a label or a temperature value. Both can be specified in
## elComandante's test list as Test@Env, where Test is any valid Test
## and Env is either a floating point number (i.e. -12.5) or an environment
## label. Only with environment labels all the features of environments
## can be used.
##
## Environment labels can be definded in elComandante.ini as follows:
## @code
## [Environment Xrf]
## Temperature: 17
## XrayVoltage: 30
## XrayCurrent: 10
## XrayTarget: Mo
## @endcode
## This example contains all the currently available parameters. The
## temperature will be used by a thermal cycling machine to control
## this aspect of the environment and an x-ray device will control
## the radiation according to the x-ray related parameters. The x-ray
## voltage is in kilovolts and the current in milliamperes. An x-ray
## target can be specified with a label. The client controlling the
## xray device (xrayClient) must know how to interpret this label.
## None or "" can be specified as well, for direct beam instead of
## a fluorescence target. Default values are 17 degrees, 30 kV, 10 mA,
## and direct beam.

class environment():
    def __init__(self, test_str, init):
        self.temperature = 17
        self.xray = False
        self.xray_voltage = 30
        self.xray_current = 10
        self.xray_target = ""
        self.name = ""
        self.updateName()
        self.decode(test_str, init)
    def __repr__(self):
        retVal = '@ENV_%s: %s degC'%(self.name,self.temperature)
        if self.xray:
            retVal += " Xray with %sV, %sA, target:'%s'"%(self.xray_voltage,self.xray_current, self.xray_target)
        return retVal
    
    def updateName(self):
        if self.temperature < 0:
            name = 'm'
        else:
            name = 'p'
        name += str(int(abs(self.temperature)))
        self.name =  name
    
    def decode(self, test_str, init):
        # Test should be a string like bla@Env
        env = test_str.split("@")
        if len(env) != 2:
            return
        env = env[1]

        # Check whether it is just a number
        try:
            self.temperature = float(env)
            self.updateName()
            return
        except:
            pass

        # Read environment definition from the init structure
        try:
            self.temperature = float(init.get("Environment " + env, "Temperature"))
            self.name = env
        except:
            pass
        try:
            self.xray_voltage = float(init.get("Environment " + env, "XrayVoltage"))
            self.xray = True
            self.name = env
        except:
            pass
        try:
            self.xray_current = float(init.get("Environment " + env, "XrayCurrent"))
            self.xray = True
            self.name = env
        except:
            pass
        try:
            self.xray_target = init.get("Environment " + env, "XrayTarget")
            self.xray = True
            self.name = env
        except:
            pass
