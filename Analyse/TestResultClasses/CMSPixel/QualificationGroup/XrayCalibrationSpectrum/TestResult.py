import AbstractClasses
import ROOT

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
