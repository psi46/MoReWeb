import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateEfficiencyModule_Chips_Chip_HighRateEffMap_TestResult"
        self.NameSingle = "HighRateEffMap"
        self.Title = "Efficiency Map"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRateEffMap'

    def OpenFileHandle(self):
        fileHandleName =  self.RawTestSessionDataPath + '/commander_HighRateTest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandleName)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Get the hitmap from the ROOT file
        histname = "effmap_C" + str(self.Attributes["ChipNo"])
        effmap = self.FileHandle.Get(histname).Clone(self.GetUniqueID())
        if not effmap:
            print "Error: could not find histogram " + histname + "!"
            return
        ntrig = self.FileHandle.Get("hr_efficiency_ntrig")
        self.ResultData['Plot']['ROOTObject'] = effmap
        self.ResultData['Plot']['ROOTObject'].SetTitle("")
        self.ResultData['Plot']['ROOTObject'].SetStats(False)
        #self.ResultData['Plot']['ROOTObject'].SetMinimum(0)
        self.ResultData['Plot']['ROOTObject'].SetMaximum(ntrig.GetVal())
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
        self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
        self.ResultData['Plot']['ROOTObject'].Draw("colz")
        self.SaveCanvas()
        
        self.ResultData["KeyValueDictPairs"] = {
            "Triggers" : {
                "Value" : int(ntrig.GetVal()),
                "Label" : "Number of calibration signals",
                "Unit" : "",
            },
        }
