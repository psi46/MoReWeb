# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='LeakageCurrentSlope'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Leakage Current Slope 150V {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)


    def GenerateOverview(self):
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HistogramMin = -1
        HistogramMax = 4
        NBins = 60

        GradeNames = {
            1 : 'A',
            2 : 'B',
            3 : 'C',
        }

        HistogramData = {
            'A': [],
            'B': [],
            'C': [],
            'N': [],
        }

        NModules = 0
        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                TestType = RowTuple['TestType']

                if TestType == self.Attributes['Test']:
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'Variation', 'Value'])
                    Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary1','KeyValueDictPairs.json','Grade','Value'])
                    if Grade and '\n' in Grade:
                        Grade = Grade.split('\n')[0]
                    if not Grade in HistogramData:
                        try:
                            Grade = GradeNames[int(Grade)]
                        except:
                            Grade = 'N'

                    if Value is not None and Grade is not None and Grade in HistogramData:
                        HistogramData[Grade].append(float(Value))
                        NModules += 1

        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['slopeivB'])
        if self.TestResultEnvironmentObject.GradingParameters.has_key('slopeivC'):
            GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['slopeivC'])
        else:
            GradeBC = 100

        HistogramOptions = {
            'GradeAB': GradeAB,
            'GradeBC': GradeBC,
            'TitleX': 'I(150 V) / I(100 V)',
            'TitleY': '# modules',
            'TextSize': 0.02,
            'TextX1': 0.15,
            'TextY1': 0.75,
            'TextX2': 0.45,
            'TextY2': 0.9,
            'LogY': True,
            'LogX': True,
            'ShadeRegions': False,
        }
        self.DrawGradingRegionPlot(HistogramData, NBins, HistogramMin, HistogramMax, HistogramOptions)

        HTML = self.Image(self.Attributes['ImageFile'])
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
        return self.Boxed(HTML)

