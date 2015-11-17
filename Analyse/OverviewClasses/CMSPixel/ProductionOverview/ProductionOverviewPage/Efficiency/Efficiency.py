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
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HTML = ""

        HistogramMin = 90
        HistogramMax = 102
        NBins = 100
        
        ModuleGrade = {
            'A' : [],
            'B' : [],
            'C' : [],
        }

        Histogram = ROOT.THStack(self.GetUniqueID(),"")


        NROCs = 0
        for ModuleID in ModuleIDsList:
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'XRayHRQualification':
                        for Chip in range(0, 16):
                            Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'EfficiencyInterpolation', 'KeyValueDictPairs.json', "InterpolatedEfficiency{Rate}".format(Rate=self.Attributes['Rate']), 'Value'])
                            Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','ROCGrade','Value'])
                            if Grade and '\n' in Grade:
                                Grade = Grade.split('\n')[0]

                            if Value is not None and Grade is not None and Grade in ModuleGrade:
                                ModuleGrade[Grade].append(float(Value))
                                NROCs += 1
                            else:
                                self.ProblematicModulesList.append(ModuleID)
        
        hA = ROOT.TH1D("vcalslope_A_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hB = ROOT.TH1D("vcalslope_B_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hC = ROOT.TH1D("vcalslope_C_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        hAB = ROOT.TH1D("vcalslope_AB_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)
        h =  ROOT.TH1D("vcalslope_all_%s"%self.GetUniqueID(), "", NBins, HistogramMin, HistogramMax)

        hA.SetFillStyle(1001)
        hA.SetFillColor(self.GetGradeColor('A'))
        hA.SetLineColor(self.GetGradeColor('A'))
        hB.SetFillStyle(1001)
        hB.SetFillColor(self.GetGradeColor('B'))
        hB.SetLineColor(self.GetGradeColor('B'))
        hC.SetFillStyle(1001)
        hC.SetFillColor(self.GetGradeColor('C'))
        hC.SetLineColor(self.GetGradeColor('C'))

        for x in ModuleGrade['A']:
            hA.Fill(x)
        for x in ModuleGrade['B']:
            hB.Fill(x)
        for x in ModuleGrade['C']:
            hC.Fill(x)

        Histogram.Add(hA)
        Histogram.Add(hB)
        Histogram.Add(hC)

        hAB.Add(hA,hB)
        h.Add(hAB,hC)

        Histogram.Draw("")


        Histogram.GetXaxis().SetTitle("Efficiency")
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        meanAll = round(h.GetMean(),2)
        meanAB = round(hAB.GetMean(),2)
        meanC = round(hC.GetMean(),2)
        meanerrAll = round(h.GetMeanError(),2)
        meanerrAB = round(hAB.GetMeanError(),2)
        meanerrC = round(hC.GetMeanError(),2)
        RMSAll = round(h.GetRMS(),2)
        RMSAB = round(hAB.GetRMS(),2)
        RMSC = round(hC.GetRMS(),2)
        underAll = int(h.GetBinContent(0))
        underAB = int(hAB.GetBinContent(0))
        underC = int(hC.GetBinContent(0))
        overAll = int(h.GetBinContent(NBins+1))
        overAB = int(hAB.GetBinContent(NBins+1))
        overC = int(hC.GetBinContent(NBins+1))


        
        stats = ROOT.TPaveText(0.15,0.7,0.45,0.9, "NDCNB")
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

       
        # Grading
        GradeAB = 98
        GradeBC = 95

        PM = Histogram.GetMaximum()*1.1
        Histogram.SetMaximum(PM)

        PlotMaximum = Histogram.GetMaximum()*3.0




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

        title4 = ROOT.TText()
        title4.SetNDC()
        title4.SetTextAlign(12)
        title4.SetTextSize(0.03)
        title4.SetTextColor(self.GetGradeColor('A'))
        title4.DrawText(0.72,0.9,"Grade A")

        title2 = ROOT.TText()
        title2.SetNDC()
        title2.SetTextAlign(12)
        title2.SetTextSize(0.03)
        title2.SetTextColor(self.GetGradeColor('B'))
        title2.DrawText(0.72,0.88,"Grade B")

        title3 = ROOT.TText()
        title3.SetNDC()
        title3.SetTextAlign(12)
        title3.SetTextSize(0.03)
        title3.SetTextColor(self.GetGradeColor('C'))
        title3.DrawText(0.72,0.86,"Grade C")


        self.SaveCanvas()

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)


        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)


