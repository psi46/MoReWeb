import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):

        self.NameSingle='VcalThresholdTrimmedPerPixel'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Vcal Thr Trimmed {Test}'.format(Test=self.Attributes['Test'])
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
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips' ,'Chip%s'%Chip, 'VcalThresholdTrimmed', '*.root'])
                            RootFiles = glob.glob(Path)
                            ROOTObject = self.GetHistFromROOTFile(RootFiles, "VcalThresholdTrimmed")
                            if ROOTObject:
                                ROOTObject.SetDirectory(0)
                                if not Histogram:
                                    Histogram = ROOTObject
                                else:
                                    try:
                                        Histogram.Add(ROOTObject)
                                    except:
                                        print "histogram could not be added, (did you try to use results of different MoReWeb versions?)"
                                self.CloseFileHandles()
        
        if Histogram:
            Histogram.Draw("HIST") # does not plot the fit line
            ROOT.gPad.Update()
            PaveStats = Histogram.FindObject("stats")
            PaveStats.SetX1NDC(0.7)
            PaveStats.SetX2NDC(0.9)
            PaveStats.SetY1NDC(0.7)
            PaveStats.SetY2NDC(0.9)
            self.SaveCanvas()
            NPix = Histogram.GetEntries()

            HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of Pixels: %d"%NPix)
            Histogram.Delete()

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

