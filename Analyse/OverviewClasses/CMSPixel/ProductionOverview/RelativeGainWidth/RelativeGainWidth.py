import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_RelativeGainWidth'
    	self.NameSingle='RelativeGainWidth'
        self.Title = 'RelativeGainWidth {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)


    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(1)
        ROOT.gPad.SetLogy(1)

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        HTML = ""

        HistogramMax = 0.25
        NBins = 120
        Histogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, HistogramMax)

        PlotColor = self.GetTestPlotColor(self.Attributes['Test'])

        Histogram.SetLineColor(PlotColor)
        Histogram.SetFillColor(PlotColor)
        Histogram.SetFillStyle(1001)
        Histogram.GetXaxis().SetTitle("Rel. Gain Width [%]")
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        for Chip in range(0, 16):
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'PHCalibrationGain', 'KeyValueDictPairs.json'])
                            JSONFiles = glob.glob(Path)
                            if len(JSONFiles) > 1:
                                print "WARNING: %s more than 1 file found '%s"%(self.Name, Path)
                            elif len(JSONFiles) < 1:
                                print "WARNING: %s json file not found: '%s"%(self.Name, Path)
                            else:
                                
                                with open(JSONFiles[0]) as data_file:    
                                    JSONData = json.load(data_file)
                                
                                if float(JSONData["mu"]['Value'])>0:
                                    Histogram.Fill(float(JSONData["sigma"]['Value']) / float(JSONData["mu"]['Value']))
                                    NROCs += 1

                        break
        
        Histogram.Draw("")
        
        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['gainB'])
        GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['gainC'])

        PlotMaximum = Histogram.GetMaximum()*1.1
        Histogram.SetMaximum(PlotMaximum)

        CloneHistogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, HistogramMax)
        for i in range(1,NBins):
            if i > GradeAB/HistogramMax*NBins and i < GradeBC/HistogramMax*NBins:
                CloneHistogram.SetBinContent(i, PlotMaximum)
          
        CloneHistogram.SetFillColorAlpha(ROOT.kBlue, 0.12)
        CloneHistogram.SetFillStyle(1001)
        CloneHistogram.Draw("same")

        CloneHistogram2 = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, HistogramMax)
        for i in range(1,NBins):
            if i >= GradeBC/HistogramMax*NBins:
                CloneHistogram2.SetBinContent(i, PlotMaximum)
          
        CloneHistogram2.SetFillColorAlpha(ROOT.kRed, 0.15)
        CloneHistogram2.SetFillStyle(1001)
        CloneHistogram2.Draw("same")

        CloneHistogram3 = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, HistogramMax)
        for i in range(1,NBins):
            if i <= GradeAB/HistogramMax*NBins:
                CloneHistogram3.SetBinContent(i, PlotMaximum)
          
        CloneHistogram3.SetFillColorAlpha(ROOT.kGreen+2, 0.1)
        CloneHistogram3.SetFillStyle(1001)
        CloneHistogram3.Draw("same")

        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

