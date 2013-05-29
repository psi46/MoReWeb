class environment():
    def __init__(self, test_str, init):
        self.temperature = 17
        self.xray = False
        self.xray_voltage = 30
        self.xray_current = 10
        self.xray_target = ""
        self.name = str(self.temperature)
        self.decode(test_str, init)
    def decode(self, test_str, init):
        # Test should be a string like bla@Env
        env = test_str.split("@")
        if len(env) != 2:
            return
        env = env[1]

        # Check whether it is just a number
        try:
            self.temperature = float(env)
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
