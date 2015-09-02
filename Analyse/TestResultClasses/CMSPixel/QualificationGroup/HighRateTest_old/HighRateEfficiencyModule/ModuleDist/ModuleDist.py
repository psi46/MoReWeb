import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_ModuleDist_TestResult"
        self.NameSingle = "ModuleDist"
        self.Title = "Efficiency Distribution"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRatePixelMapModule'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        chips = self.ParentObject.ResultData['SubTestResults']['Chips']
        ntrig = chips.ResultData['SubTestResults']['Chip0'].ResultData['SubTestResults']['HighRateEffMap'].ResultData['KeyValueDictPairs']['Triggers']['Value']
        hist = ROOT.TH1F(self.GetUniqueID(), "", ntrig + 1, 0, ntrig + 1)
        for roc in range(len(chips.ResultData['SubTestResults'])):
            chip = chips.ResultData['SubTestResults']['Chip' + str(roc)]
            effmap = chip.ResultData['SubTestResults']['HighRateEffMap'].ResultData['Plot']['ROOTObject']

            # Iterate over the cols and rows of the single ROC
            for col in range(52):
                for row in range(80):
                    # Get pixel hits from single ROC
                    content = effmap.GetBinContent(col + 1, row + 1)

                    # Fill pixel hits from single ROC into module
                    hist.Fill(content)

        # Set some histogram attributes
        hist.GetXaxis().SetTitle("Efficiency")
        hist.GetXaxis().CenterTitle()
        hist.GetYaxis().SetTitle("# Pixels")
        hist.GetYaxis().CenterTitle()
        hist.GetYaxis().SetTitleOffset(1.5)
        hist.SetStats(False)


        # Add the histogram to the result of this test
        self.ResultData['Plot']['ROOTObject'] = hist
        self.ResultData['Plot']['ROOTObject'].Draw()
        self.SaveCanvas()
        