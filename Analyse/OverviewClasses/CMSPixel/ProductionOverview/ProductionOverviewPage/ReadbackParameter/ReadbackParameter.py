import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='ReadbackParameter'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
    
        self.Title = 'ReadbackParameter {Parameter} {Test}'.format(Test=self.Attributes['Test'], Parameter=self.Attributes['Parameter'])
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
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HTML = ""

        NBins = 120
        Histogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, self.Attributes['Xmin'], self.Attributes['Xmax'])

        PlotColor = self.GetTestPlotColor(self.Attributes['Test'])
        Histogram.SetLineColor(PlotColor)
        Histogram.SetFillColor(PlotColor)
        Histogram.SetFillStyle(1001)
        Histogram.GetXaxis().SetTitle(self.Attributes['Parameter'])
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        for Chip in range(0, 16):
                            IsCalibrated = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'ReadbackCal', 'KeyValueDictPairs.json', 'ReadbackCalibrated', 'Value'])
                            if IsCalibrated and IsCalibrated.lower().strip() == 'true':
                                Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'ReadbackCal', 'KeyValueDictPairs.json', self.Attributes['Parameter'], 'Value'])
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

        # mean, rms and gauss fit sigma
        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        title.SetTextSize(0.035)
        TitleText = "NRocs: %d, Mean: %1.2e, RMS: %1.2e"%(NROCs, Histogram.GetMean(), Histogram.GetRMS())
        title.DrawText(0.15, 0.965, TitleText)

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

