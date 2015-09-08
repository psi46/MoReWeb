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
        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        HTML = ""
        HistogramMax = self.Attributes['Maximum']
        NBins = self.Attributes['NBins']
        Histogram = ROOT.TH1D(self.GetUniqueID(), "", NBins, 0, HistogramMax)

        PlotColor = self.GetTestPlotColor(self.Attributes['Test'])
        Histogram.SetLineColor(PlotColor)
        Histogram.SetFillColor(PlotColor)
        Histogram.SetFillStyle(1001)
        Histogram.GetXaxis().SetTitle("DAC Value")
        Histogram.GetYaxis().SetTitle("# ROCs")
        Histogram.GetYaxis().SetTitleOffset(1.5)

        NROCs = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']

                    if TestType == self.Attributes['Test']:

                        for Chip in range(0, 16):
                            Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'DacParameterOverview', 'DacParameters{Trim}'.format(Trim=self.Attributes['Trim']), 'KeyValueDictPairs.json', self.Attributes['DAC'], 'Value'])
                            if Value is not None:
                                Histogram.Fill(float(Value))
                                NROCs += 1

                        break
        
        Histogram.Draw("")

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        Subtitle = self.Attributes['Test']
        TestNames = {'m20_1' : 'Fulltest -20°C BTC', 'm20_2': 'Fulltest -20°C ATC', 'p17_1': 'Fulltest +17°C'}
        if TestNames.has_key(Subtitle):
            Subtitle = TestNames[Subtitle]
        title.DrawText(0.15,0.965,Subtitle)

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        return self.Boxed(HTML)

