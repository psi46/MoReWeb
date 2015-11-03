import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):

        self.NameSingle='GainPerPixel'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Gain per pixel {Test}'.format(Test=self.Attributes['Test'])
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
        Histogram = None
        PlotColor = self.GetTestPlotColor(self.Attributes['Test'])

        NROCs = 0
        for ModuleID in ModuleIDsList:
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == self.Attributes['Test']:
                        for Chip in range(0, 16):
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips' ,'Chip%s'%Chip, 'PHCalibrationGain', '*.root'])
                            RootFiles = glob.glob(Path)
                            ROOTObject = self.GetHistFromROOTFile(RootFiles, "PHCalibrationGain")
                            if ROOTObject:
                                ROOTObject.SetDirectory(0)
                                if not Histogram:
                                    Histogram = ROOTObject
                                else:
                                    try:
                                        Histogram.Add(ROOTObject)
                                        NROCs += 1
                                    except:
                                        self.ProblematicModulesList.append(ModuleID)
            self.CloseFileHandles()

        if Histogram:
            Histogram.Draw("")

            CutLow = ROOT.TCutG('lLower', 2)
            CutLow.SetPoint(0, self.TestResultEnvironmentObject.GradingParameters['gainMin'], -1e6)
            CutLow.SetPoint(1, self.TestResultEnvironmentObject.GradingParameters['gainMin'], +1e6)
            CutLow.SetLineColor(ROOT.kRed)
            CutLow.SetLineStyle(2)
            CutLow.Draw('same')

            CutHigh = ROOT.TCutG('lUpper', 2)
            CutHigh.SetPoint(0, self.TestResultEnvironmentObject.GradingParameters['gainMax'], -1e6)
            CutHigh.SetPoint(1, self.TestResultEnvironmentObject.GradingParameters['gainMax'], +1e6)
            CutHigh.SetLineColor(ROOT.kRed)
            CutHigh.SetLineStyle(2)
            CutHigh.Draw('same')

            Histogram.SetStats(ROOT.kTRUE)

            ROOT.gPad.Update()
            PaveStats = Histogram.FindObject("stats")
            PaveStats.SetX1NDC(0.18)
            PaveStats.SetX2NDC(0.40)
            PaveStats.SetY1NDC(0.7)
            PaveStats.SetY2NDC(0.9)

            title = ROOT.TText()
            title.SetNDC()
            title.SetTextAlign(11)
            title.SetTextAlign(12)
            title.SetTextSize(0.04)
            NPix = Histogram.GetEntries()
            title.DrawText(0.15, 0.965, "#roc: %d,  #pix: %d"%(NROCs, NPix))

            self.SaveCanvas()
            HTML = self.Image(self.Attributes['ImageFile'])
            Histogram.Delete()
        else:
            Message = "No histogram for gain per pixel found!!!"
            HTML = Message
            self.PrintInfo(Message)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList
        return self.Boxed(HTML)

