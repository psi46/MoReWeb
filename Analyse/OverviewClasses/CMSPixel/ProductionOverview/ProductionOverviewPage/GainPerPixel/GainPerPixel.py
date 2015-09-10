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
        ModuleErrors =set()
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
                                    except:
                                        ModuleErrors.add(ModuleID)
            self.CloseFileHandles()

        if len(ModuleErrors) > 0:
            print "    found problems with following modules:"
            for ModuleID in ModuleErrors:
                print "      ",ModuleID

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

            self.SaveCanvas()
            NPix = Histogram.GetEntries()
            HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of Pixels: %d"%NPix)
            Histogram.Delete()
        else:
            Message = "No histogram for gain per pixel found!!! %r"%ModuleID
            HTML = Message
            self.PrintInfo(Message)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

