import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='Efficiency'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Efficiency {Rate}'.format(Rate=self.Attributes['Rate'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(111210)
        ROOT.gPad.SetLogy(1)

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        HTML = ""

        HistogramMin = 90
        HistogramMax = 102
        NBins = 100
        Histogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)

        PlotColor = ROOT.kGreen+2
        Histogram.SetLineColor(PlotColor)
        Histogram.SetFillColor(PlotColor)
        Histogram.SetFillStyle(1001)
        Histogram.GetXaxis().SetTitle("Efficiency")
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        NROCs = 0
        for ModuleID in ModuleIDsList:
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'XRayHRQualification':
                        for Chip in range(0, 16):
                            Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'EfficiencyInterpolation', 'KeyValueDictPairs.json', "InterpolatedEfficiency{Rate}".format(Rate=self.Attributes['Rate']), 'Value'])
                            if Value is not None:
                                Histogram.Fill(float(Value))
                                NROCs += 1
        
        Histogram.Draw("")
        ROOT.gPad.Update()
        PaveStats = Histogram.FindObject("stats")
      	PaveStats.SetX1NDC(0.18)
      	PaveStats.SetX2NDC(0.42)
      	PaveStats.SetY1NDC(0.78)
      	PaveStats.SetY2NDC(0.88)
       
        # Grading
        GradeAB = 98
        GradeBC = 95

        PlotMaximum = Histogram.GetMaximum()*1.1
        Histogram.SetMaximum(PlotMaximum)

        try:
            CloneHistogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i >= CloneHistogram.GetXaxis().FindBin(GradeBC) and i <= CloneHistogram.GetXaxis().FindBin(GradeAB):
                    CloneHistogram.SetBinContent(i, PlotMaximum)
              
            CloneHistogram.SetFillColorAlpha(ROOT.kBlue, 0.12)
            CloneHistogram.SetFillStyle(1001)
            CloneHistogram.Draw("same")

            CloneHistogram2 = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i < CloneHistogram.GetXaxis().FindBin(GradeBC):
                    CloneHistogram2.SetBinContent(i, PlotMaximum)
              
            CloneHistogram2.SetFillColorAlpha(ROOT.kRed, 0.15)
            CloneHistogram2.SetFillStyle(1001)
            CloneHistogram2.Draw("same")

            CloneHistogram3 = ROOT.TH1D(self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
            for i in range(1,NBins):
                if i > CloneHistogram.GetXaxis().FindBin(GradeAB):
                    CloneHistogram3.SetBinContent(i, PlotMaximum)
              
            CloneHistogram3.SetFillColorAlpha(ROOT.kGreen+2, 0.1)
            CloneHistogram3.SetFillStyle(1001)
            CloneHistogram3.Draw("same")
        except:
            pass

        # subtitle
        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        title.SetTextSize(0.03)
        Subtitle = "Efficiency at {Rate} MHz/cm^2, ROCs:{NROCs}".format(Rate=self.Attributes['Rate'], NROCs=NROCs)
        title.DrawText(0.15,0.95,Subtitle)

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)


