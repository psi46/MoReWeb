import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_HighRatePixelMapModule_Chips_Chip_HighRatePixelMapSummary_TestResult"
        self.NameSingle = "HighRatePixelMapSummary"
        self.Title = "Summary"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'HighRatePixelMapSummary'

    def OpenFileHandle(self):
        fileHandleName =  self.RawTestSessionDataPath + "/" + self.Attributes["TestResultSubDirectory"] + '/commander_HighRateTest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandleName)

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        # Get the hitmap from the ROOT file
        histname = "hitmap_C" + str(self.Attributes["ChipNo"])
        hitmap = self.FileHandle.Get(histname)
        if not hitmap:
            print "Error: could not find histogram " + histname + "!"
            return

        hits = hitmap.GetEntries()
        triggers = self.FileHandle.Get("pixelmap_triggers")
        if not triggers:
            triggers = -1
        else:
            triggers = triggers.GetVal()

        core_hits = 0
        core_hits_2 = 0
        for col in range(2, 50):
            for row in range(79):
                h = hitmap.GetBinContent(col + 1, row + 1)
                core_hits += h
                core_hits_2 += h * h

        core_pixels = (52 - 2 * 2) * (80 - 1)
        hits_per_pixel_mean = core_hits / core_pixels
        hits_per_pixel_stdev = ((core_pixels * core_hits_2 - core_hits * core_hits) / (core_pixels * (core_pixels - 1))) ** 0.5

        pixels_with_zero_hits = 0
        pixels_with_low_eff = 0
        for col in range(52):
            for row in range(80):
                h = hitmap.GetBinContent(col + 1, row + 1)
                if h == 0:
                    pixels_with_zero_hits += 1
                # FIXME: Set LIMIT configureable <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                elif h < hits_per_pixel_mean - 4 * hits_per_pixel_stdev:
                    pixels_with_low_eff += 1

        active_area = (52 - 2 * 2) * (80 - 1) * 0.01 * 0.015; # cm2
        active_time = triggers * 25e-9; # s
        clock_stretch = 1 # Not available yet from ROOT file <<<<<<<<<<<<<<<<<<<
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
            "Triggers" : {
                "Value" : int(triggers),
                "Label" : "Number of triggers",
                "Unit" : "[1]",
            },
            "Hits" : {
                "Value" : int(hits),
                "Label" : "Number of x-ray hits",
                "Unit" : "[1]",
            },
            "Insensitive pixels" : {
                "Value" : pixels_with_zero_hits,
                "Label" : "Insensitive pixels",
                "Unit" : "[1]",
            },
            "Inefficient pixels" : {
                "Value" : pixels_with_low_eff,
                "Label" : "Inefficient pixels",
                "Unit" : "[1]",
            },
        }

        self.ResultData['KeyList'] = [
            'Rate',
            'Triggers',
            'Hits',
            'Insensitive pixels',
            'Inefficient pixels',
        ]
