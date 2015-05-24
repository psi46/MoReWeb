import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateEfficiencyModule_Chips_Chip_TestResult"
        self.NameSingle = "Chip"
        self.Title = "Chip " + str(self.Attributes["ChipNo"])
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        self.ResultData["SubTestResultDictList"] = [
                {
                    "Key": "HighRateEffMap",
                    "InitialAttributes": {
                        "StorageKey": "HighRateEffMap",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRateEffMap",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 1,
                        "Width":1
                    }
                }, {
                    "Key": "HighRateEffDist",
                    "InitialAttributes": {
                        "StorageKey": "HighRateEffDist",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRateEffDist",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 1,
                        "Width":1
                    }
                }, {
                    "Key": "HighRateEffSummary",
                    "InitialAttributes": {
                        "StorageKey": "HighRateEffSummary",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRateEffSummary",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 2,
                        "Width":2
                    }
                }
        ]
        self.Attributes['TestedObjectType'] = 'Chip'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        HighRateEffMap = self.ResultData['SubTestResults']['HighRateEffMap']
        self.ResultData['Plot']['ROOTObject'] = HighRateEffMap.ResultData['Plot']['ROOTObject'].Clone(self.GetUniqueID())
        self.ResultData['Plot']['ROOTObject'].Draw("colz")
        self.SaveCanvas()
        self.ResultData['Plot']['Enabled'] = 0
