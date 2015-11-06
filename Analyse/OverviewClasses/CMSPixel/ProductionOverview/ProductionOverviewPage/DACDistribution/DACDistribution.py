# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):

        self.NameSingle='DACDistribution'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'DAC distribution {Test} {DAC} {Trim}'.format(Test=self.Attributes['Test'], DAC=self.Attributes['DAC'], Trim=self.Attributes['Trim'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,400)


    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(1)

        TableData = []
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HTML = ""
        HistogramMax = self.Attributes['Maximum']
        NBins = self.Attributes['NBins']

        ModuleGrade = {
            '1' : [],
            '2' : [],
            '3' : [],
        }

        Histogram = ROOT.THStack(self.GetUniqueID(),"")

        

        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        for Chip in range(0, 16):
                            Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'DacParameterOverview', 'DacParameters{Trim}'.format(Trim=self.Attributes['Trim']), 'KeyValueDictPairs.json', self.Attributes['DAC'], 'Value'])
                            Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value'])
                            if Value is not None and Grade is not None:
                                ModuleGrade[Grade].append(float(Value))
                                NROCs += 1
                            if Value is not None and Grade is None:
                                ModuleGrade['3'].append(float(Value))
                                NROCs += 1
                        break

        hA = ROOT.TH1D("vcalslope_A_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)
        hB = ROOT.TH1D("vcalslope_B_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)
        hC = ROOT.TH1D("vcalslope_C_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)
        hAB = ROOT.TH1D("vcalslope_AB_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)
        h = ROOT.TH1D("vcalslope_all_%s"%self.GetUniqueID(), "", NBins, 0, HistogramMax)

        hA.SetFillStyle(1001)
        hA.SetFillColor(self.GetGradeColor('A'))
        hA.SetLineColor(self.GetGradeColor('A'))
        hB.SetFillStyle(1001)
        hB.SetFillColor(self.GetGradeColor('B'))
        hB.SetLineColor(self.GetGradeColor('B'))
        hC.SetFillStyle(1001)
        hC.SetFillColor(self.GetGradeColor('C'))
        hC.SetLineColor(self.GetGradeColor('C'))

        for x in ModuleGrade['1']:
            hA.Fill(x)
        for x in ModuleGrade['2']:
            hB.Fill(x)
        for x in ModuleGrade['3']:
            hC.Fill(x)

        Histogram.Add(hA)
        Histogram.Add(hB)
        Histogram.Add(hC)

        hAB.Add(hA,hB)
        h.Add(hAB,hC)
        
        Histogram.Draw("")

        Histogram.GetXaxis().SetTitle("DAC Value")
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


        
        stats = ROOT.TPaveText(0.6,0.6,0.9,0.8, "NDCNB")
        stats.SetFillColor(ROOT.kWhite)
        stats.SetTextSize(0.025)
        stats.SetTextAlign(10)
        stats.SetTextFont(62)
        stats.SetBorderSize(0)
        stats.AddText("All: #mu = {0} #pm {1}".format(meanAll,meanerrAll))
        stats.AddText(" #sigma = {0}".format(RMSAll))
        stats.AddText("AB: #mu = {0} #pm {1}".format(meanAB,meanerrAB))
        stats.AddText(" #sigma = {0}".format(RMSAB))
        stats.AddText("C: #mu = {0} #pm {1}".format(meanC,meanerrC))
        stats.AddText(" #sigma = {0}".format(RMSC))
        stats.Draw("same")

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        Subtitle = self.Attributes['Test']
        TestNames = {'m20_1' : 'Fulltest -20°C BTC', 'm20_2': 'Fulltest -20°C ATC', 'p17_1': 'Fulltest +17°C'}
        if TestNames.has_key(Subtitle):
            Subtitle = TestNames[Subtitle]
        title.DrawText(0.15,0.965,Subtitle)

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
        title2.DrawText(0.72,0.87,"Grade B")

        title3 = ROOT.TText()
        title3.SetNDC()
        title3.SetTextAlign(12)
        title3.SetTextSize(0.03)
        title3.SetTextColor(self.GetGradeColor('C'))
        title3.DrawText(0.72,0.84,"Grade C")

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        return self.Boxed(HTML)

