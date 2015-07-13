import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_Chips_Chip_TestResult"
        self.NameSingle = "Chip"
        self.Title = "Chip " + str(self.Attributes["ChipNo"])
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        self.ResultData["SubTestResultDictList"] = [
                {
                    "Key": "HighRatePixelMap",
                    "InitialAttributes": {
                        "StorageKey": "HighRatePixelMap",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRatePixelMap",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        #"SubTestResultDictList": self.Attributes["SubTestResultDictList"]
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 1,
                        "Width": 1
                    }
                }, {
                    "Key": "HighRatePixelMapDist",
                    "InitialAttributes": {
                        "StorageKey": "HighRatePixelMapDist",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRatePixelMapDist",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        #"SubTestResultDictList": self.Attributes["SubTestResultDictList"]
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 2,
                        "Width": 1
                    }
                }, {
                    "Key": "HighRatePHMap",
                    "InitialAttributes": {
                        "StorageKey": "HighRatePHMap",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRatePHMap",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        #"SubTestResultDictList": self.Attributes["SubTestResultDictList"]
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 3,
                        "Width": 1
                    }
                }, {
                    "Key": "HighRatePHDist",
                    "InitialAttributes": {
                        "StorageKey": "HighRatePHDist",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRatePHDist",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        #"SubTestResultDictList": self.Attributes["SubTestResultDictList"]
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 4,
                        "Width": 1
                    }
                }, {
                    "Key": "HighRatePHWidthMap",
                    "InitialAttributes": {
                        "StorageKey": "HighRatePHWidthMap",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRatePHWidthMap",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        #"SubTestResultDictList": self.Attributes["SubTestResultDictList"]
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 5,
                        "Width": 1
                    }
                }, {
                    "Key": "HighRatePixelMapSummary",
                    "InitialAttributes": {
                        "StorageKey": "HighRatePixelMapSummary",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRatePixelMap",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        #"SubTestResultDictList": self.Attributes["SubTestResultDictList"]
                        'XrayVoltage': self.Attributes["XrayVoltage"],
                        'XrayCurrent': self.Attributes["XrayCurrent"],
                        'ChipNo': self.Attributes["ChipNo"],
                    },
                    "DisplayOptions":{
                        "Order": 7,
                        "Width": 2
                    }
                }
        ]
        self.Attributes['TestedObjectType'] = 'Chip'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        HighRatePixelMap = self.ResultData['SubTestResults']['HighRatePixelMap']
        self.ResultData['Plot']['ROOTObject'] = HighRatePixelMap.ResultData['Plot']['ROOTObject'].Clone(self.GetUniqueID())
        self.ResultData['Plot']['ROOTObject'].Draw("colz")
        self.SaveCanvas()
        self.ResultData['Plot']['Enabled'] = 0
        
