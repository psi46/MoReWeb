import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_ModuleMap_TestResult"
        self.NameSingle = "ModuleMap"
        self.Title = "Efficiency Map"
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

        width = 52 * 8
        height = 80 * 2

        ntrig = 20
        hist = ROOT.TH2F(self.GetUniqueID(), "", width, 0, width, height, 0, height)
        chips = self.ParentObject.ResultData['SubTestResults']['Chips']
        for roc in range(len(chips.ResultData['SubTestResults'])):
            chip = chips.ResultData['SubTestResults']['Chip' + str(roc)]
            pixmap = chip.ResultData['SubTestResults']['HighRateEffMap'].ResultData['Plot']['ROOTObject']
            ntrig = chip.ResultData['SubTestResults']['HighRateEffMap'].ResultData['KeyValueDictPairs']['Triggers']['Value']

            # Iterate over the cols and rows of the single ROC
            for col in range(52):
                for row in range(80):
                    # Get pixel hits from single ROC
                    content = pixmap.GetBinContent(col + 1, row + 1)

                    # Calculate module coordinates
                    if roc < 8:
                        mrow = 159 - row
                        mcol = (8 - roc) * 52 - col - 1
                    else:
                        mrow = row
                        mcol = (roc - 8) * 52 + col

                    # Fill pixel hits from single ROC into module
                    hist.SetBinContent(mcol + 1, mrow + 1, content)

        # Set some histogram attributes
        hist.SetMaximum(ntrig)
        hist.GetXaxis().SetTitle("Column No.")
        hist.GetXaxis().CenterTitle()
        hist.GetYaxis().SetTitle("Row No.")
        hist.GetYaxis().CenterTitle()
        hist.GetYaxis().SetTitleOffset(0.5)
        hist.SetStats(False)


        # Add the histogram to the result of this test
        self.ResultData['Plot']['ROOTObject'] = hist
        self.ResultData['Plot']['ROOTObject'].Draw("colz")
        self.SaveCanvas()
        