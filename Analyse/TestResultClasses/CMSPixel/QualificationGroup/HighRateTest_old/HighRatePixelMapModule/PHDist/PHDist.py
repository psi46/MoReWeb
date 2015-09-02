import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_PHDist_TestResult"
        self.NameSingle = "PHDist"
        self.Title = "Pulseheight Distribution"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRatePHDistModule'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        hist = ROOT.TH1F(self.GetUniqueID(), "", 2048, -1024, 1024)
        chips = self.ParentObject.ResultData['SubTestResults']['Chips']
        for roc in range(len(chips.ResultData['SubTestResults'])):
            chip = chips.ResultData['SubTestResults']['Chip' + str(roc)]
            pixmap = chip.ResultData['SubTestResults']['HighRatePHDist'].ResultData['Plot']['ROOTObject']

            # Iterate over the histogram bins
            for bin in range(2048):
                # Get pixel hits from single ROC
                content = pixmap.GetBinContent(bin + 1)

                # Fill pixel hits from single ROC into module
                fill = hist.GetBinContent(bin + 1)
                hist.SetBinContent(bin + 1, fill + content)

        # Set some histogram attributes
        hist.GetXaxis().SetRangeUser(0, 256) # FIXME: depends on module type <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        hist.GetXaxis().SetTitle("Pulse height")
        hist.GetXaxis().CenterTitle()
        hist.GetYaxis().SetTitle("# Pixels")
        hist.GetYaxis().CenterTitle()
        hist.GetYaxis().SetTitleOffset(2.0)
        hist.SetStats(False)


        # Add the histogram to the result of this test
        self.ResultData['Plot']['ROOTObject'] = hist
        self.ResultData['Plot']['ROOTObject'].Draw()
        self.SaveCanvas()
        