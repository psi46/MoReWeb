import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateDColEfficiencyModule_Chips_Chip_HighRateDColEfficiency_TestResult"
        self.NameSingle = "HighRateDColEfficiency"
        self.Title = "Relative Efficiency"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRateDColEfficiency'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Find the high rate test TestResults object
        chip = self.ParentObject
        chips = chip.ParentObject
        dcoleff = chips.ParentObject
        hrtest = dcoleff.ParentObject

        # Get the hitmap for the low intensity
        pmtest_a = hrtest.ResultData['SubTestResults'][self.Attributes['PixelMapA']]
        pmtest_a_chips = pmtest_a.ResultData['SubTestResults']['Chips']
        pmtest_a_chip = pmtest_a_chips.ResultData['SubTestResults']['Chip' + str(self.Attributes["ChipNo"])]
        pmtest_a_pmmap = pmtest_a_chip.ResultData['SubTestResults']['HighRatePixelMap']
        hitmap_low = pmtest_a_pmmap.ResultData['Plot']['ROOTObject']

        # Get the hitmap for the high intensity
        pmtest_b = hrtest.ResultData['SubTestResults'][self.Attributes['PixelMapB']]
        pmtest_b_chips = pmtest_b.ResultData['SubTestResults']['Chips']
        pmtest_b_chip = pmtest_b_chips.ResultData['SubTestResults']['Chip' + str(self.Attributes["ChipNo"])]
        pmtest_b_pmmap = pmtest_b_chip.ResultData['SubTestResults']['HighRatePixelMap']
        hitmap_high = pmtest_b_pmmap.ResultData['Plot']['ROOTObject']

        # Get the x-ray currents
        current_a = pmtest_a_pmmap.Attributes["XrayCurrent"]
        current_b = pmtest_b_pmmap.Attributes["XrayCurrent"]

        hist = ROOT.TH1F(self.GetUniqueID(), "", 26, 0, 26)

        for dcol in range(26):
            sum_a = 0
            sum_a_2 = 0
            sum_b = 0
            sum_b_2 = 0
            for col in range(2):
                for row in range(80):
                    sum_a += hitmap_low.GetBinContent(dcol * 2 + col + 1, row + 1)
                    sum_a_2 += hitmap_low.GetBinContent(dcol * 2 + col + 1, row + 1) ** 2
                    sum_b += hitmap_high.GetBinContent(dcol * 2 + col + 1, row + 1)
                    sum_b_2 += hitmap_high.GetBinContent(dcol * 2 + col + 1, row + 1) ** 2
            hist.SetBinContent(dcol + 1, sum_b / sum_a * current_a / current_b)
            err_a = sum_a ** 0.5
            err_b = sum_b ** 0.5
            err_fraction = ((err_b / sum_a) ** 2 + (err_a * sum_b / (sum_a ** 2)) ** 2) ** 0.5
            hist.SetBinError(dcol + 1, err_fraction * current_a / current_b)


        self.ResultData['Plot']['ROOTObject'] = hist
        self.ResultData['Plot']['ROOTObject'].SetStats(False)
        #self.ResultData['Plot']['ROOTObject'].SetMinimum(0)
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Double Column No.")
        self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Relative Efficiency")
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
