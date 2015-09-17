# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='LeakageCurrent'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Leakage Current 150V {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)


    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(111210)
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogx(0)

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        HTML = ""

        HistogramMin = 1e-7
        HistogramMax = 3e-5
        NBins = 60

        Histogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, HistogramMax)

        PlotColor = self.GetTestPlotColor(self.Attributes['Test'])
        Histogram.SetLineColor(PlotColor)
        Histogram.SetFillColor(PlotColor)
        Histogram.SetFillStyle(1001)
        Histogram.GetXaxis().SetTitle("current [A]")
        Histogram.GetYaxis().SetTitle("# modules")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        NModules = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        Factor = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Factor'])
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])

                        if Factor is not None and Value is not None:
                            Histogram.Fill(float(Factor) * float(Value))
                            NModules += 1

        Histogram.Draw("")

        ROOT.gPad.Update()
        PaveStats = Histogram.FindObject("stats")
        PaveStats.SetX1NDC(0.62)
        PaveStats.SetX2NDC(0.83)
        PaveStats.SetY1NDC(0.8)
        PaveStats.SetY2NDC(0.9)

        GradeAB = 1.e-6*float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
        GradeBC = 1.e-6*float(self.TestResultEnvironmentObject.GradingParameters['currentC'])

        PlotMaximum = Histogram.GetMaximum()*1.1
        Histogram.SetMaximum(PlotMaximum)

        try:
            CloneHistogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i <= CloneHistogram.GetXaxis().FindBin(GradeBC) and i >= CloneHistogram.GetXaxis().FindBin(GradeAB):
                    CloneHistogram.SetBinContent(i, PlotMaximum)
              
            CloneHistogram.SetFillColorAlpha(ROOT.kBlue, 0.12)
            CloneHistogram.SetFillStyle(1001)
            CloneHistogram.Draw("same")

            CloneHistogram2 = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i > CloneHistogram.GetXaxis().FindBin(GradeBC):
                    CloneHistogram2.SetBinContent(i, PlotMaximum)
              
            CloneHistogram2.SetFillColorAlpha(ROOT.kRed, 0.15)
            CloneHistogram2.SetFillStyle(1001)
            CloneHistogram2.Draw("same")

            CloneHistogram3 = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i < CloneHistogram.GetXaxis().FindBin(GradeAB):
                    CloneHistogram3.SetBinContent(i, PlotMaximum)
              
            CloneHistogram3.SetFillColorAlpha(ROOT.kGreen+2, 0.1)
            CloneHistogram3.SetFillStyle(1001)
            CloneHistogram3.Draw("same")
        except:
            pass

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        Subtitle = self.Attributes['Test']
        TestNames = {'m20_1' : 'Fulltest -20°C BTC', 'm20_2': 'Fulltest -20°C ATC', 'p17_1': 'Fulltest +17°C'}
        if TestNames.has_key(Subtitle):
            Subtitle = TestNames[Subtitle]
        title.DrawText(0.15,0.965,"%s, modules: %d"%(Subtitle,NModules))

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
        return self.Boxed(HTML)

