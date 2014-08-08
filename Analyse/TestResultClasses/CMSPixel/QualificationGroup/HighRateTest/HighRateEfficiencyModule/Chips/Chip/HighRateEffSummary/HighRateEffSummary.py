import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRateEfficiencyModule_Chips_Chip_HighRateEffSummary_TestResult"
        self.NameSingle = "HighRateEffSummary"
        self.Title = "Efficiency Summary"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRateEffSummary'

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

        # Calculate efficiency
        eff = 0
        eff_2 = 0
        core_eff = 0
        core_eff_2 = 0
        ntrig = self.FileHandle.Get("hr_efficiency_ntrig").GetVal()
        for col in range(52):
            for row in range(80):
                eff += 100.0 * effmap.GetBinContent(col + 1, row + 1) / ntrig
                eff_2 += (100.0 * effmap.GetBinContent(col + 1, row + 1) / ntrig) ** 2
                if col > 1 and col < 50 and row < 79:
                    core_eff += 100.0 * effmap.GetBinContent(col + 1, row + 1) / ntrig
                    core_eff_2 += (100.0 * effmap.GetBinContent(col + 1, row + 1) / ntrig) ** 2

        all_pixels = 4160
        core_pixels = (52 - 2 * 2) * (80 - 1)
        eff_val = eff / all_pixels
        eff_err = ((all_pixels * eff_2 - eff * eff) / (all_pixels * (all_pixels - 1))) ** 0.5 / all_pixels ** 0.5
        core_eff_val = core_eff / core_pixels
        core_eff_err = ((core_pixels * core_eff_2 - core_eff * core_eff) / (core_pixels * (core_pixels - 1))) ** 0.5 / core_pixels ** 0.5

        bkgmap = self.FileHandle.Get("bkgmap_C" + str(self.Attributes["ChipNo"])).Clone(self.GetUniqueID())
        hits = bkgmap.GetEntries()
        triggers = ntrig * 4160 # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

        core_hits = 0
        core_hits_2 = 0
        for col in range(2, 50):
            for row in range(79):
                h = bkgmap.GetBinContent(col + 1, row + 1)
                core_hits += h
                core_hits_2 += h * h

        core_pixels = (52 - 2 * 2) * (80 - 1)
        hits_per_pixel_mean = core_hits / core_pixels
        hits_per_pixel_stdev = ((core_pixels * core_hits_2 - core_hits * core_hits) / (core_pixels * (core_pixels - 1))) ** 0.5

        pixels_with_zero_hits = 0
        pixels_with_low_eff = 0
        for col in range(52):
            for row in range(80):
                h = bkgmap.GetBinContent(col + 1, row + 1)
                if h == 0:
                    pixels_with_zero_hits += 1
                # FIXME: Set LIMIT configureable <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                elif h < hits_per_pixel_mean - 4 * hits_per_pixel_stdev:
                    pixels_with_low_eff += 1

        active_area = (52 - 2 * 2) * (80 - 1) * 0.01 * 0.015; # cm2
        active_time = triggers * 25e-9; # s
        clock_stretch = 1 # Not available yet from ROOT file <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        if clock_stretch > 1:
            active_time *= clock_stretch
        rate_val = core_hits / active_time / active_area / 1e6
        rate_err = core_hits ** 0.5 / active_time / active_area / 1e6

        self.ResultData["KeyValueDictPairs"] = {
            "Rate" : {
                "Value" : round(rate_val, 2),
                "Sigma" : round(rate_err, 2),
                "Label" : "Measured rate",
                "Unit" : "MHz / cm2",
            },
            "Core efficiency" : {
                "Value" : round(core_eff_val, 2),
                "Sigma" : round(core_eff_err, 2),
                "Label" : "Core efficiency",
                "Unit" : "%",
            },
            "Mean efficiency" : {
                "Value" : round(eff_val, 2),
                "Sigma" : round(eff_err, 2),
                "Label" : "Mean efficiency",
                "Unit" : "%",
            },
            "Hits" : {
                "Value" : int(hits),
                "Label" : "Number of x-ray hits",
                "Unit" : "",
            },
        }

        self.ResultData['KeyList'] = [
            'Rate',
            'Core efficiency',
            'Mean efficiency',
            'Hits',
        ]
