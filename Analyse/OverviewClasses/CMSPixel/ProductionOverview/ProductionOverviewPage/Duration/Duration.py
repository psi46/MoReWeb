import ROOT
import AbstractClasses
import time
import datetime
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='Duration'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
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

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        HTML = ""

        HistogramMax = 140
        NBins = 38
        NFullTests = 0

        TestDurations = {
            'm20_1' : [],
            'm20_2' : [],
            'p17_1' : [],
        }

        # fill list with durations
        for ModuleID in ModuleIDsList:
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    # only count Fulltests
                    if TestDurations.has_key(TestType):
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'DigitalCurrent', 'HiddenData.json', 'Duration', 'Value'])
                        
                        if Value:
                            TestDurations[TestType].append(float(Value)/60.0)
                            NFullTests += 1

        # create plot

        HistStack = ROOT.THStack("hs_fulltest_duration","")

        hA = ROOT.TH1D("h1duration_m20_1_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)
        hB = ROOT.TH1D("h1duration_m20_2_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)
        hC = ROOT.TH1D("h1duration_p17_1_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)

        hA.SetFillStyle(1001)
        hA.SetFillColor(self.GetTestPlotColor('m20_1'))
        hB.SetFillStyle(1001)
        hB.SetFillColor(self.GetTestPlotColor('m20_2'))
        hC.SetFillStyle(1001)
        hC.SetFillColor(self.GetTestPlotColor('p17_1'))

        for DurationMinutes in TestDurations['m20_1']:
            hA.Fill(DurationMinutes)
        for DurationMinutes in TestDurations['m20_2']:
            hB.Fill(DurationMinutes)
        for DurationMinutes in TestDurations['p17_1']:
            hC.Fill(DurationMinutes)

        HistStack.Add(hA)
        HistStack.Add(hB)
        HistStack.Add(hC)

        HistStack.Draw()
        HistStack.GetXaxis().SetLabelOffset(0.02)
        HistStack.GetXaxis().SetTitle("minutes")
        HistStack.GetXaxis().SetTitleOffset(1)
        HistStack.GetYaxis().SetTitle("# modules")
        HistStack.GetYaxis().SetTitleOffset(0.7)
                        
        HistStack.Draw("")
        
        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of Fulltests: %d"%NFullTests)
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

