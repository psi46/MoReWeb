import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_PixelMapDist_TestResult"
        self.NameSingle = "PixelMapDist"
        self.Title = "Pixel Hit Distribution"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRatePixelMapDistModule'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        width = 52 * 8
        height = 80 * 2

        chips = self.ParentObject.ResultData['SubTestResults']['Chips']

        # Determine maximum
        max = 0
        for roc in range(len(chips.ResultData['SubTestResults'])):
            chip = chips.ResultData['SubTestResults']['Chip' + str(roc)]
            pixmap = chip.ResultData['SubTestResults']['HighRatePixelMap'].ResultData['Plot']['ROOTObject']

            # Iterate over the cols and rows of the single ROC
            for col in range(52):
                for row in range(80):
                    # Get pixel hits from single ROC
                    content = pixmap.GetBinContent(col + 1, row + 1)

                    # Correct for pixel size
                    #if row == 79:
                    #    content /= 2
                    #if col == 0 or col == 51:
                    #    content /= 2

                    if content > max:
                        max = content

        hist = ROOT.TH1F(self.GetUniqueID(), "", 100, 0, max + 1)

        # Fill histogram
        for roc in range(len(chips.ResultData['SubTestResults'])):
            chip = chips.ResultData['SubTestResults']['Chip' + str(roc)]
            pixmap = chip.ResultData['SubTestResults']['HighRatePixelMap'].ResultData['Plot']['ROOTObject']

            # Iterate over the cols and rows of the single ROC
            for col in range(52):
                for row in range(80):
                    # Get pixel hits from single ROC
                    content = pixmap.GetBinContent(col + 1, row + 1)

                    # Correct for pixel size
                    #if row == 79:
                    #    content /= 2
                    #if col == 0 or col == 51:
                    #    content /= 2

                    # Fill pixel hits from single ROC into module
                    hist.Fill(content)

        # Set some histogram attributes
        #hist.SetMinimum(0)
        hist.GetXaxis().SetTitle("No. of hits")
        hist.GetXaxis().CenterTitle()
        hist.GetYaxis().SetTitle("# Pixels")
        hist.GetYaxis().CenterTitle()
        hist.GetYaxis().SetTitleOffset(2.0)
        hist.SetStats(False)


        # Add the histogram to the result of this test
        self.ResultData['Plot']['ROOTObject'] = hist
        self.ResultData['Plot']['ROOTObject'].Draw()
        self.SaveCanvas()
        