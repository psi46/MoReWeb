import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateDColEfficiencyModule_Chips_Chip_HighRateDColEfficiencySummary_TestResult"
        self.NameSingle = "HighRateDColEfficiencySummary"
        self.Title = "Efficiency Summary"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRateDColEfficiencySummary'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Get the test result from the relative efficiency
        eff = self.ParentObject.ResultData['SubTestResults']['HighRateDColEfficiency'].ResultData['Plot']['ROOTObject']

        s1 = 0
        s2 = 0
        median_list = []
        for dcol in range(26):
            median_list.append(eff.GetBinContent(dcol + 1))
            s1 += eff.GetBinContent(dcol + 1)
            s2 += eff.GetBinContent(dcol + 1) ** 2

        # Calculate sigma
        sigma = ((26 * s2 - s1 * s1) / (26 * 25)) ** 0.5

        # Calculate mean
        mean = s1 / 26
        mean_err = sigma / (26 ** 0.5)

        median_list.sort()
        median = median_list[len(median_list) / 2]

        ineff_dcols = 0
        for dcol in range(26):
            sigma = (eff.GetBinContent(dcol + 1) - median) / eff.GetBinError(dcol + 1)
            if sigma < -4: # make configureable <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                ineff_dcols += 1


        self.ResultData["KeyValueDictPairs"] = {
            "mean" : {
                "Value" : round(mean * 100, 1),
                "Sigma" : round(mean_err * 100, 1),
                "Label" : "Mean efficiency",
                "Unit" : "%",
            },
            "median" : {
                "Value" : round(median * 100),
                "Sigma" : 0,
                "Label" : "Median efficiency",
                "Unit" : "%",
            },
            "ineff_dcols" : {
                "Value" : int(ineff_dcols),
                "Sigma" : 0,
                "Label" : "Inefficient DCols",
                "Unit" : "[1]",
            },
        }

        self.ResultData['KeyList'] = [
            'mean',
            'median',
            'ineff_dcols',
        ]
