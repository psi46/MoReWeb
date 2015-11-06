import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):

        self.NameSingle='PedestalPerPixel'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Pedestal per pixel {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)

    def GenerateOverview(self):
        #ROOT.gStyle.SetOptStat(111210)
        ROOT.gPad.SetLogy(1)
        ROOT.gStyle.SetOptStat("");

        
        HistogramMin = 0
        HistogramMax = 1
        NBins = 450

        TableData = []

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        HTML = ""
        Histogram = ROOT.TH1D("ped_All_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        HistogramA = ROOT.TH1D("ped_A_%s"%self.GetUniqueID(), "",  NBins, HistogramMin, HistogramMax)
        HistogramB = ROOT.TH1D("ped_B_%s"%self.GetUniqueID(), "",  NBins, HistogramMin, HistogramMax)
        HistogramC = ROOT.TH1D("ped_C_%s"%self.GetUniqueID(), "",  NBins, HistogramMin, HistogramMax)
        HistogramAB = ROOT.TH1D("ped_AB_%s"%self.GetUniqueID(), "",  NBins, HistogramMin, HistogramMax)

        NROCs = 0
        for ModuleID in ModuleIDsList:
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        for Chip in range(0, 16):
                            Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value'])
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips' ,'Chip%s'%Chip, 'PHCalibrationPedestal', '*.root'])
                            RootFiles = glob.glob(Path)
                            ROOTObject = self.GetHistFromROOTFile(RootFiles, "PHCalibrationGain") # (called PHCalibrationGain) todo: name consistently
                            if ROOTObject:
                                ROOTObject.SetDirectory(0)
                                if not Histogram:
                                    Histogram = ROOTObject
                                else:
                                    try:
                                        Histogram.Add(ROOTObject)
                                    except:
                                        print "histogram could not be added, (did you try to use results of different MoReWeb versions?)"
                                if not HistogramA:
                                    HistogramA = ROOTObject
                                elif Grade == '1':
                                    try:
                                        HistogramA.Add(ROOTObject)
                                    except:
                                        print "histogram could not be added, (did you try to use results of different MoReWeb versions?)"
                                if not HistogramB:
                                    HistogramB = ROOTObject
                                elif Grade == '2':
                                    try:
                                        HistogramB.Add(ROOTObject)
                                    except:
                                        print "histogram could not be added, (did you try to use results of different MoReWeb versions?)"
                                if not HistogramC:
                                    HistogramC = ROOTObject
                                elif Grade == '3':
                                    try:
                                        HistogramC.Add(ROOTObject)
                                    except:
                                        print "histogram could not be added, (did you try to use results of different MoReWeb versions?)"
                                if not HistogramAB:
                                    HistogramAB = ROOTObject
                                elif Grade == '1' or Grade == '2':
                                    try:
                                        HistogramAB.Add(ROOTObject)
                                    except:
                                        print "histogram could not be added, (did you try to use results of different MoReWeb versions?)"
                                self.CloseFileHandles()
        

        if Histogram:
            Histogram.GetXaxis().SetRangeUser(-150,300)
            Histogram.GetXaxis().CenterTitle()
            Histogram.GetXaxis().SetTitle("Vcal offset")
            Histogram.GetYaxis().SetTitle("No. of Entries")
            Histogram.GetYaxis().CenterTitle()
            Histogram.GetYaxis().SetTitleOffset(1.2)
            Histogram.Draw("")
            HistogramA.SetLineColor(self.GetGradeColor('A'))
            HistogramA.Draw("same")
            HistogramB.SetLineColor(self.GetGradeColor('B'))
            HistogramB.Draw("same")
            HistogramC.SetLineColor(self.GetGradeColor('C'))
            HistogramC.Draw("same")

            ROOT.gPad.Update()
            meanAll = round(Histogram.GetMean(),2)
            meanAB = round(HistogramAB.GetMean(),2)
            meanC = round(HistogramC.GetMean(),2)
            meanerrAll = round(Histogram.GetMeanError(),2)
            meanerrAB = round(HistogramAB.GetMeanError(),2)
            meanerrC = round(HistogramC.GetMeanError(),2)
            RMSAll = round(Histogram.GetRMS(),2)
            RMSAB = round(HistogramAB.GetRMS(),2)
            RMSC = round(HistogramC.GetRMS(),2)
            underAll = int(Histogram.GetBinContent(0))
            underAB = int(HistogramAB.GetBinContent(0))
            underC = int(HistogramC.GetBinContent(0))
            overAll = int(Histogram.GetBinContent(Histogram.GetSize()))
            overAB = int(HistogramAB.GetBinContent(HistogramAB.GetSize()))
            overC = int(HistogramC.GetBinContent(HistogramC.GetSize()))


            
            stats = ROOT.TPaveText(0.6,0.6,0.9,0.8, "NDCNB")
            stats.SetFillColor(ROOT.kWhite)
            stats.SetTextSize(0.025)
            stats.SetTextAlign(10)
            stats.SetTextFont(62)
            stats.SetBorderSize(0)
            stats.AddText("All: #mu = {0} #pm {1}".format(meanAll,meanerrAll))
            stats.AddText(" #sigma = {0}".format(RMSAll))
            stats.AddText("  UF = {0}, OF = {1}".format(underAll,overAll))
            stats.AddText("AB: #mu = {0} #pm {1}".format(meanAB,meanerrAB))
            stats.AddText(" #sigma = {0}".format(RMSAB))
            stats.AddText("  UF = {0}, OF = {1}".format(underAB,overAB))
            stats.AddText("C: #mu = {0} #pm {1}".format(meanC,meanerrC))
            stats.AddText(" #sigma = {0}".format(RMSC))
            stats.AddText("  UF = {0}, OF = {1}".format(underC,overC))
            stats.Draw("same")

            title3 = ROOT.TText()
            title3.SetNDC()
            title3.SetTextAlign(12)
            title3.SetTextSize(0.03)
            title3.DrawText(0.72,0.9,"All")

            title4 = ROOT.TText()
            title4.SetNDC()
            title4.SetTextAlign(12)
            title4.SetTextSize(0.03)
            title4.SetTextColor(self.GetGradeColor('A'))
            title4.DrawText(0.72,0.88,"Grade A")

            title2 = ROOT.TText()
            title2.SetNDC()
            title2.SetTextAlign(12)
            title2.SetTextSize(0.03)
            title2.SetTextColor(self.GetGradeColor('B'))
            title2.DrawText(0.72,0.86,"Grade B")

            title3 = ROOT.TText()
            title3.SetNDC()
            title3.SetTextAlign(12)
            title3.SetTextSize(0.03)
            title3.SetTextColor(self.GetGradeColor('C'))
            title3.DrawText(0.72,0.84,"Grade C")

            self.SaveCanvas()
            NPix = Histogram.GetEntries()

            HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of Pixels: %d"%NPix)
            Histogram.Delete()
            HistogramA.Delete()
            HistogramB.Delete()
            HistogramC.Delete()
            HistogramAB.Delete()

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)
