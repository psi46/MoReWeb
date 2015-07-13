import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateDColEfficiencyModule_Chips_Chip_TestResult"
        self.NameSingle = "Chip"
        self.Title = "Chip " + str(self.Attributes["ChipNo"])
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = [
                {
                    "Key": "HighRateDColEfficiency",
                    "InitialAttributes": {
                        "StorageKey": "HighRateDColEfficiency",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRateDColEfficiency",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": self.Attributes["ChipNo"],
                        "PixelMapA": self.Attributes["PixelMapA"],
                        "PixelMapB": self.Attributes["PixelMapB"],
                    },
                    "DisplayOptions":{
                        "Order": 1,
                        "Width": 1
                    }
                }, {
                    "Key": "HighRateDColEfficiencySigma",
                    "InitialAttributes": {
                        "StorageKey": "HighRateDColEfficiencySigma",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRateDColEfficiencySigma",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": self.Attributes["ChipNo"],
                        "PixelMapA": self.Attributes["PixelMapA"],
                        "PixelMapB": self.Attributes["PixelMapB"],
                    },
                    "DisplayOptions":{
                        "Order": 2,
                        "Width": 1
                    }
                }, {
                    "Key": "HighRateDColEfficiencySummary",
                    "InitialAttributes": {
                        "StorageKey": "HighRateDColEfficiencySummary",
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "HighRateDColEfficiency",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": self.Attributes["ChipNo"],
                        "PixelMapA": self.Attributes["PixelMapA"],
                        "PixelMapB": self.Attributes["PixelMapB"],
                    },
                    "DisplayOptions":{
                        "Order": 3,
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

        HighRateDColEfficiency = self.ResultData['SubTestResults']['HighRateDColEfficiency']
        self.ResultData['Plot']['ROOTObject'] = HighRateDColEfficiency.ResultData['Plot']['ROOTObject'].Clone(self.GetUniqueID())
        self.ResultData['Plot']['ROOTObject'].Draw("colz")
        self.SaveCanvas()
        self.ResultData['Plot']['Enabled'] = 0
