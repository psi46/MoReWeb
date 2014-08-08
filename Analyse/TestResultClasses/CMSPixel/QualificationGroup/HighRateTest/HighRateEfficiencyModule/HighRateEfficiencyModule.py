import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateEfficiencyModule_TestResult"
        self.NameSingle = "HighRateEfficiencyModule"
        self.Title = "Pixel efficiency (%.1f C, %i kV, %i mA)" % (self.Attributes["TestTemperature"], self.Attributes["XrayVoltage"], self.Attributes["XrayCurrent"])
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        ModuleVersion, nRocs, halfModule = self.ReadModuleConfigParams()

        self.ResultData["SubTestResultDictList"] = [
            {
                "Key": "Chips",
                "InitialAttributes": {
                    "StorageKey": "Chips",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "ModuleNRocs": nRocs,
                    "TestType": "HighRateTest",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'XrayVoltage': self.Attributes["XrayVoltage"],
                    'XrayCurrent': self.Attributes["XrayCurrent"],
                },
                "DisplayOptions":{
                    "Order": 1,
                    "Width": 4
                }
            }, {
                "Key": "Power",
                "InitialAttributes": {
                    "StorageKey": "Power",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "HighRateTest",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'XrayVoltage': self.Attributes["XrayVoltage"],
                    'XrayCurrent': self.Attributes["XrayCurrent"],
                },
                "DisplayOptions":{
                    "Order": 2,
                    "Width": 1
                }
            }, {
                "Key": "ModuleMap",
                "InitialAttributes": {
                    "StorageKey": "ModuleMap",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "HighRateTest",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'XrayVoltage': self.Attributes["XrayVoltage"],
                    'XrayCurrent': self.Attributes["XrayCurrent"],
                },
                "DisplayOptions":{
                    "Order": 3,
                    "Width": 4
                }
            }, {
                "Key": "ModuleDist",
                "InitialAttributes": {
                    "StorageKey": "ModuleDist",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "HighRateTest",
                    "TestTemperature": self.Attributes["TestTemperature"],
                    'XrayVoltage': self.Attributes["XrayVoltage"],
                    'XrayCurrent': self.Attributes["XrayCurrent"],
                },
                "DisplayOptions":{
                    "Order": 4,
                    "Width": 1
                }
            }
        ]
        self.Attributes['TestedObjectType'] = 'HighRateEfficiencyModule'

    def ReadModuleConfigParams(self):
        fileName = self.RawTestSessionDataPath + '/configParameters.dat'
        f = open(fileName)
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith('rocType'):
                version = line.split(' ')[-1]
            elif line.strip().startswith('nRocs'):
                nRocs = int(line.split(' ')[-1])
            elif line.strip().startswith('halfModule'):
                halfModule = int(line.split(' ')[-1])
        f.close()
        return (version, nRocs, halfModule)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
