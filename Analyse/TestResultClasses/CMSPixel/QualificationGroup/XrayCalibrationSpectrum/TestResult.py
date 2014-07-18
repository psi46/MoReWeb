import AbstractClasses
import ROOT
import os
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_TestResult"
        self.NameSingle = "XrayCalibrationSpectrum"
        self.Title = "X-ray Calibration (Pulse Height Method)"
        self.verbose = False
        self.check_Test_Software()
        self.ROCtype, self.nRocs,self.halfModule = self.ReadModuleVersion()
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        self.ResultData["SubTestResultDictList"] = self.Attributes["SubTestResultDictList"]
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationModule",
                "Module": "VcalCalibrationModule",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationModule",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                },
                "DisplayOptions":{
                    "Order": 0,
                    "Width": 5
                }
            }
        )
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationSlope",
                "Module": "VcalCalibrationSlope",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationSlope",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                },
                "DisplayOptions":{
                    "Order": 1,
                    "Width": 1
                }
            }
        )
        self.ResultData["SubTestResultDictList"].append(
            {
                "Key": "VcalCalibrationOffset",
                "Module": "VcalCalibrationOffset",
                "InitialAttributes": {
                    "StorageKey": "VcalCalibrationOffset",
                    "TestResultSubDirectory": ".",
                    "IncludeIVCurve": False,
                    "ModuleID": self.Attributes["ModuleID"],
                    "ModuleVersion": self.Attributes["ModuleVersion"],
                    "ModuleType": self.Attributes["ModuleType"],
                    "TestType": "Chips",
                    "TestTemperature": self.Attributes["TestTemperature"],
                },
                "DisplayOptions":{
                    "Order": 1,
                    "Width": 1
                }
            }
        )


        self.check_Test_Software()

        self.Attributes['TestedObjectType'] = 'XrayCalibrationSpectrum'


    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        #self.ResultData['Table'] = {
        #    'HEADER':[
        #        [
        #            'ROC',
        #        ]
        #    ],
        #    'BODY':[],
        #    'FOOTER':[],
        #}
