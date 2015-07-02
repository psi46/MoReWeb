import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='MeanNoiseROC'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'MeanNoiseROC {Test}'.format(Test=self.Attributes['Test'])
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

        NoiseMax = 1200
        NBins = 120
        Histogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, NoiseMax)

        PlotColor = self.GetTestPlotColor(self.Attributes['Test'])
        Histogram.SetLineColor(PlotColor)
        Histogram.SetFillColor(PlotColor)
        Histogram.SetFillStyle(1001)
        Histogram.GetXaxis().SetTitle("Noise [e-]")
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        for Chip in range(0, 16):
                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'SCurveWidths', 'KeyValueDictPairs.json', 'mu', 'Value'])

                            if Value is not None:
                                Histogram.Fill(float(Value))
                                NROCs += 1

                        break
        
        Histogram.Draw("")

        ROOT.gPad.Update()
        PaveStats = Histogram.FindObject("stats")
        PaveStats.SetX1NDC(0.62)
        PaveStats.SetX2NDC(0.83)
        PaveStats.SetY1NDC(0.8)
        PaveStats.SetY2NDC(0.9)
        
        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['noiseB'])
        GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['noiseC'])

        PlotMaximum = Histogram.GetMaximum()*1.1
        Histogram.SetMaximum(PlotMaximum)

        CloneHistogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, NoiseMax)
        for i in range(1,NBins):
            if i > GradeAB/NoiseMax*NBins and i < GradeBC/NoiseMax*NBins:
                CloneHistogram.SetBinContent(i, PlotMaximum)
          
        CloneHistogram.SetFillColorAlpha(ROOT.kBlue, 0.12)
        CloneHistogram.SetFillStyle(1001)
        CloneHistogram.Draw("same")

        CloneHistogram2 = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, NoiseMax)
        for i in range(1,NBins):
            if i >= GradeBC/NoiseMax*NBins:
                CloneHistogram2.SetBinContent(i, PlotMaximum)
          
        CloneHistogram2.SetFillColorAlpha(ROOT.kRed, 0.15)
        CloneHistogram2.SetFillStyle(1001)
        CloneHistogram2.Draw("same")

        CloneHistogram3 = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, NoiseMax)
        for i in range(1,NBins):
            if i <= GradeAB/NoiseMax*NBins:
                CloneHistogram3.SetBinContent(i, PlotMaximum)
          
        CloneHistogram3.SetFillColorAlpha(ROOT.kGreen+2, 0.1)
        CloneHistogram3.SetFillStyle(1001)
        CloneHistogram3.Draw("same")

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

