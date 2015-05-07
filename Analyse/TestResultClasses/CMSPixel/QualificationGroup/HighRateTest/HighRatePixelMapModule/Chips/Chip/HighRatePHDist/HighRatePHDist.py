import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_Chips_Chip_HighRatePHDist_TestResult"
        self.NameSingle = "HighRatePHDist"
        self.Title = "Pulseheight Distribution"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRatePHDist'

    def OpenFileHandle(self):
        fileHandleName =  self.RawTestSessionDataPath + "/" + self.Attributes["TestResultSubDirectory"] + '/commander_HighRateTest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandleName)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Get the hitmap from the ROOT file
        histname = "ph_dist_C" + str(self.Attributes["ChipNo"])
        phmap = self.FileHandle.Get(histname).Clone(self.GetUniqueID())
        if not phmap:
            print "Error: could not find histogram " + histname + "!"
            return
        self.ResultData['Plot']['ROOTObject'] = phmap
        self.ResultData['Plot']['ROOTObject'].SetTitle("")
        self.ResultData['Plot']['ROOTObject'].SetStats(False)
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, 256) # FIXME: Range depends on module type <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Pulse height")
        self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("# X-ray hits")
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(2.5)
        self.ResultData['Plot']['ROOTObject'].Draw()
        if self.SavePlotFile:
             self.SaveCanvas()
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
