# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):

        self.NameSingle='Dac2D'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'DAC distribution {Test} {DACX} {DACY} {Trim}'.format(Test=self.Attributes['Test'], DACX=self.Attributes['DACX'], DACY=self.Attributes['DACY'], Trim=self.Attributes['Trim'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,400)


    def GenerateOverview(self):
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HistogramMinX = self.Attributes['MinimumX'] if 'MinimumX' in self.Attributes else 0
        HistogramMaxX = self.Attributes['MaximumX'] if 'MaximumX' in self.Attributes else 255
        NBinsX = self.Attributes['NBinsX'] if 'NBinsX' in self.Attributes else (HistogramMaxX-HistogramMinX+1)

        HistogramMinY = self.Attributes['MinimumY'] if 'MinimumY' in self.Attributes else 0
        HistogramMaxY = self.Attributes['MaximumY'] if 'MaximumY' in self.Attributes else 255
        NBinsY = self.Attributes['NBinsY'] if 'NBinsY' in self.Attributes else (HistogramMaxY-HistogramMinY+1)

        HistogramData = []
        NROCs = 0
        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                TestType = RowTuple['TestType']
                if TestType == self.Attributes['Test']:
                    for Chip in range(0, 16):
                        ValueX = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'DacParameterOverview', 'DacParameters{Trim}'.format(Trim=self.Attributes['Trim']), 'KeyValueDictPairs.json', self.Attributes['DACX'], 'Value'])
                        ValueY = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'DacParameterOverview', 'DacParameters{Trim}'.format(Trim=self.Attributes['Trim']), 'KeyValueDictPairs.json', self.Attributes['DACY'], 'Value'])

                        if ValueX is not None and ValueY is not None:
                            HistogramData.append([int(ValueX), int(ValueY)])
                            NROCs += 1
                        else:
                            self.ProblematicModulesList.append(RowTuple['ModuleID'])

        Histogram = ROOT.TH2D(self.GetUniqueID(), "", NBinsX, HistogramMinX, HistogramMaxX, NBinsY, HistogramMinY, HistogramMaxY)
        for HistogramTuple in HistogramData:
            Histogram.Fill(HistogramTuple[0], HistogramTuple[1])

        self.Canvas.SetFrameLineStyle(0)
        self.Canvas.SetFrameLineWidth(1)
        self.Canvas.SetFrameBorderMode(0)
        self.Canvas.SetFrameBorderSize(1)
        ROOT.gPad.SetLogx(0)
        ROOT.gPad.SetLogy(0)

        Histogram.GetXaxis().SetTitle(self.Attributes['DACX'])
        Histogram.GetYaxis().SetTitle(self.Attributes['DACY'])
        Histogram.GetYaxis().SetTitleOffset(1.1)
        Histogram.Draw("colz")

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        self.DisplayErrorsList()
        return self.Boxed(HTML)