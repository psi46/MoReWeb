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

        # Get module information
        ModuleVersion, self.nRocs, halfModule = self.ReadModuleConfigParams()

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
