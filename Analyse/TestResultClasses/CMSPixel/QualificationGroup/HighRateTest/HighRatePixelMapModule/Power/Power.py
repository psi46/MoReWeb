import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_Power_TestResult"
        self.NameSingle = "Power"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRatePowerModule'

    def OpenFileHandle(self):
        fileHandleName =  self.RawTestSessionDataPath + "/" + self.Attributes["TestResultSubDirectory"] + '/commander_HighRateTest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandleName)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        iana = self.FileHandle.Get("hr_pixelmap_analog_current")
        vana = self.FileHandle.Get("hr_pixelmap_analog_voltage")
        idig = self.FileHandle.Get("hr_pixelmap_digital_current")
        vdig = self.FileHandle.Get("hr_pixelmap_digital_voltage")

        if iana == None or vana == None or idig == None or vdig == None:
            print "Error: could not find voltage/current information in ROOT file!"

        if iana == None:
            iana = -1.0
        else:
            iana = iana.GetVal()

        if vana == None:
            vana = -1.0
        else:
            vana = vana.GetVal()

        if idig == None:
            idig = -1.0
        else:
            idig = idig.GetVal()

        if vdig == None:
            vdig = -1.0
        else:
            vdig = vdig.GetVal()

        self.ResultData["KeyValueDictPairs"] = {
            "Analog current" : {
                "Value" : round(iana * 1000.0, 1),
                "Label" : "Analog current",
                "Unit" : "mA",
            },
            "Analog voltage" : {
                "Value" : round(vana, 2),
                "Label" : "Analog voltage",
                "Unit" : "V",
            },
            "Digital current" : {
                "Value" : round(idig * 1000.0, 1),
                "Label" : "Digital current",
                "Unit" : "mA",
            },
            "Digital voltage" : {
                "Value" : round(vdig, 2),
                "Label" : "Digital voltage",
                "Unit" : "V",
            },
        }

        self.ResultData['KeyList'] = [
            'Analog current',
            'Analog voltage',
            'Digital current',
            'Digital voltage'
        ]
