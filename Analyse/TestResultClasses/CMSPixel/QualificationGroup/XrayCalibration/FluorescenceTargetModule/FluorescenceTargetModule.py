import AbstractClasses
import ROOT
from AbstractClasses.GeneralTestResult import GeneralTestResult

class TestResult(GeneralTestResult):
    def CustomInit(self):
        method = self.Attributes['Method']
        self.Name = "CMSPixel_QualificationGroup_XrayCalibration_" + method + "_FluorescenceTargetModule_" + \
                    self.Attributes["Target"]
        self.Name += "_TestResult"
        self.NameSingle = "FluorescenceTargetModule"
        # + self.Attributes["Target"] + '_' + method
        self.Title = "Xray Module %s - %s" % (method, self.Attributes["Target"])
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        self.check_Test_Software()
        # self.nRocs = self.ParentObject.nRocs
        # self.ROCtype = self.ParentObject.version
        # self.halfModule = self.ParentObject.halfModule
        # Get module information
        self.ResultData['HiddenData']['ModuleVersion'] = self.version
        self.ResultData['HiddenData']['nRocs'] = self.nRocs
        self.ResultData['HiddenData']['halfModule'] = self.halfModule
        for roc in range(self.nRocs):
            key = "FluorescenceTarget_C{ROC}".format(ROC=roc)
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": key,
                    "Module": "FluorescenceTargetROC",
                    "InitialAttributes": {
                        "StorageKey": key,
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": roc,
                        'Target': self.Attributes['Target'],
                        'Method': method
                    },
                    "DisplayOptions": {
                        "Order": roc + 1,
                        "Width": 1
                    }
                }
            )
        # TODO: @ Esteban - Explain what is the TestedObjectType for?
        self.Attributes['TestedObjectType'] = 'FluorescenceTargetModule'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData['KeyValueDictPairs'] = {
            'ModuleNROCs': {
                "Value": self.nRocs,
                "Sigma": 0,
                "Label": "Number of ROCs",
                "Unit": "",
            }
        }

        # self.ResultData['Table'] = {
        #    'HEADER':[
        #        [
        #            'ROC', 'Vcal'
        #        ]
        #    ],
        #    'BODY':[],
        #    'FOOTER':[],
        #}
