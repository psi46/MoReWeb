import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_QualificationGroup_XrayCalibrationSpectrum_FluorescenceSpectrumModule_TestResult"
        self.NameSingle = "FluorescenceSpectrumModule"
        self.Title = "Module Spectrum %s" % (self.Attributes["Target"])
        self.verbose = False
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData["SubTestResultDictList"] = []
        self.check_Test_Software()
        self.nRocs=self.ParentObject.nRocs
        self.ROCtype=self.ParentObject.ROCtype
        self.halfModule=self.ParentObject.halfModule
        # Get module information
        self.ResultData['HiddenData']['ModuleVersion'] = self.ROCtype
        self.ResultData['HiddenData']['nRocs'] = self.nRocs
        self.ResultData['HiddenData']['halfModule'] = self.halfModule
        for roc in range(self.nRocs):
            self.ResultData["SubTestResultDictList"].append(
                {
                    "Key": "FluorescenceSpectrum_C" + str(roc),
                    "Module": "FluorescenceSpectrum",
                    "InitialAttributes": {
                        "StorageKey": "Chip" + str(roc),
                        "TestResultSubDirectory": ".",
                        "IncludeIVCurve": False,
                        "ModuleID": self.Attributes["ModuleID"],
                        "ModuleVersion": self.Attributes["ModuleVersion"],
                        "ModuleType": self.Attributes["ModuleType"],
                        "TestType": "Chips",
                        "TestTemperature": self.Attributes["TestTemperature"],
                        "ChipNo": roc,
                        'Target': self.Attributes['Target'],
                        'TargetEnergy': self.Attributes['TargetEnergy'],
                        'TargetNElectrons': self.Attributes['TargetNElectrons'],
                    },
                    "DisplayOptions":{
                        "Order": roc + 1,
                        "Width": 1
                    }
                }
            )

        self.Attributes['TestedObjectType'] = 'FluorescenceSpectrumModule'


    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag
        self.ResultData['KeyValueDictPairs'] = {
            'ModuleNROCs' : {
                "Value" : self.nRocs,
                "Sigma" : 0,
                "Label" : "Number of ROCs",
                "Unit" : "",
            }
        }

        #self.ResultData['Table'] = {
        #    'HEADER':[
        #        [
        #            'ROC', 'Vcal'
        #        ]
        #    ],
        #    'BODY':[],
        #    'FOOTER':[],
        #}
