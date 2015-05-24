import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateDColEfficiencyModule_Chips_Chip_HighRateDColEfficiencySigma_TestResult"
        self.NameSingle = "HighRateDColEfficiencySigma"
        self.Title = "Efficiency Sigma"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRateDColEfficiencySigma'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Get the test result from the relative efficiency
        eff = self.ParentObject.ResultData['SubTestResults']['HighRateDColEfficiency'].ResultData['Plot']['ROOTObject']

        median_list = []
        for dcol in range(26):
            median_list.append(eff.GetBinContent(dcol + 1))
        median_list.sort()
        median = median_list[len(median_list) / 2]

        hist = ROOT.TH1F(self.GetUniqueID(), "", 20, -10, 10)
        for dcol in range(26):
            sigma = (eff.GetBinContent(dcol + 1) - median) / eff.GetBinError(dcol + 1)
            hist.Fill(sigma)

        self.ResultData['Plot']['ROOTObject'] = hist
        self.ResultData['Plot']['ROOTObject'].SetStats(False)
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Double Column Efficiency (Sigma)")
        self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("# DCols")
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
        self.ResultData['Plot']['ROOTObject'].Draw()
        self.SaveCanvas()
        
        #self.ResultData["KeyValueDictPairs"] = {
        #    "Rate" : {
        #        "Value" : 0,
        #        "Sigma" : 0,
        #        "Label" : "",
        #        "Unit" : "",
        #    },
        #}
        #
        #self.ResultData['KeyList'] = [
        #    'Rate',
        #    'Triggers',
        #    'Hits',
        #    'Insensitive pixels',
        #    'Inefficient pixels',
        #]
