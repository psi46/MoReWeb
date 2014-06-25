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
                    "Order": 1,
                    "Width": 5
                }
            }
        )

        self.check_Test_Software()

        self.Attributes['TestedObjectType'] = 'XrayCalibrationSpectrum'

    def check_Test_Software(self):
#         print self.RawTestSessionDataPath
        file = self.RawTestSessionDataPath + '/test.cfg'
#         print file
        if os.path.exists(file):
            self.testSoftware = 'pyxar'
        elif os.path.exists(self.RawTestSessionDataPath + '/pxar.log'):
            self.testSoftware = 'pxar'
        else:
            self.testSoftware = 'psi46expert'
        self.HistoDict = BetterConfigParser()
        fileName = 'Configuration/HistoNames/%s.cfg' % self.testSoftware
        print fileName, os.path.exists(fileName), os.getcwd()
        print 'test software is %s' % self.testSoftware
        self.HistoDict.read(fileName)

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
