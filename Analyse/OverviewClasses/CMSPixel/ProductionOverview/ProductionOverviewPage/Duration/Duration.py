import ROOT
import AbstractClasses


class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle = 'Duration'
        self.Name = 'CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Fulltest Duration'
        self.DisplayOptions = {
            'Width': 2,
        }
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(800, 400)
        self.SubPages = []

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(1)
        ROOT.gPad.SetLogy(0)

        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        HTML = ""

        HistogramMax = 140
        NBins = 38
        NFullTests = 0

        TestDurations = {}
        for FullTestName in self.FullQualificationFullTests:
            TestDurations[FullTestName] = []

        # fill list with durations
        for ModuleID in ModuleIDsList:
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    FullTestName = RowTuple['TestType']
                    # only count Fulltests
                    if TestDurations.has_key(FullTestName):
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'DigitalCurrent', 'HiddenData.json', 'Duration', 'Value'])
                        if Value:
                            TestDurations[FullTestName].append(float(Value)/60.0)
                            NFullTests += 1
                        else:
                            if self.Verbose:
                                print "     could not get duration for %s at %s"%(ModuleID, FullTestName)
                            self.ProblematicModulesList.append(ModuleID)

        # create plots for different fulltest temperatures
        FulltestDurationHistograms = {}
        for FullTestName in self.FullQualificationFullTests:
            FulltestDurationHistograms[FullTestName] = ROOT.TH1D("h1duration_%s_%s"%(FullTestName, self.GetUniqueID()), "", NBins, 0, HistogramMax)
            FulltestDurationHistograms[FullTestName].SetFillStyle(1001)
            FulltestDurationHistograms[FullTestName].SetFillColor(self.GetTestPlotColor(FullTestName))

            for DurationMinutes in TestDurations[FullTestName]:
                FulltestDurationHistograms[FullTestName].Fill(DurationMinutes)

        # stack them
        HistStack = ROOT.THStack("hs_fulltest_duration_%s"%self.GetUniqueID(),"")
        for FullTestName in self.FullQualificationFullTests:
            HistStack.Add(FulltestDurationHistograms[FullTestName])

        # draw
        HistStack.Draw()
        HistStack.GetXaxis().SetLabelOffset(0.02)
        HistStack.GetXaxis().SetTitle("minutes")
        HistStack.GetXaxis().SetTitleOffset(1)
        HistStack.GetYaxis().SetTitle("# modules")
        HistStack.GetYaxis().SetTitleOffset(0.7)
        HistStack.Draw("")

        OffsetX = 0.15
        for FullTestName in self.FullQualificationFullTests:
            title = ROOT.TText()
            title.SetNDC()
            title.SetTextAlign(11)
            title.SetTextAlign(12)
            title.SetTextColor(self.GetTestPlotColor(FullTestName))
            title.DrawText(OffsetX, 0.965, FullTestName)
            OffsetX += 0.1

        # save
        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of Fulltests: %d"%NFullTests)
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)

