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

        HistogramMax = 120
        NBins = 120
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

                        Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Temperature', 'KeyValueDictPairs.json'])
                        JSONFiles = glob.glob(Path)
                        if len(JSONFiles) > 1:
                            print "WARNING: %s more than 1 file found '%s"%(self.Name, Path)
                        elif len(JSONFiles) < 1:
                            print "WARNING: %s json file not found: '%s"%(self.Name, Path)
                        else:
                            
                            with open(JSONFiles[0]) as data_file:    
                                JSONData = json.load(data_file)
                            
                            
                            TestDurationString = JSONData["Duration"]['Value']
                            if len(TestDurationString.split(':')) == 3:
                                Hours = float(TestDurationString.split(':')[0])
                                Minutes = float(TestDurationString.split(':')[1])
                                Seconds = float(TestDurationString.split(':')[2])

                                TestDurations[TestType].append(Hours*60.0 + Minutes + Seconds/60.0)

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
        for DurationSeconds in TestDurations['m20_2']:
            hB.Fill(DurationMinutes)
        for DurationSeconds in TestDurations['p17_1']:
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

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of Fulltestss: %d"%NFullTests)
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

