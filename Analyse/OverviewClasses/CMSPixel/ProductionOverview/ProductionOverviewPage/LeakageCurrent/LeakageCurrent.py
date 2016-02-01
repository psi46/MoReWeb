# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='LeakageCurrent'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Leakage Current 150V {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)


    def GenerateOverview(self):
        print "    Fulltest: ", self.Attributes['Test']

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)


        HistogramMin = 1e-7
        HistogramMax = 3e-5
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

                    Factor = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Factor'])
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                    Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary1','KeyValueDictPairs.json','Grade','Value'])
                    if Grade and '\n' in Grade:
                        Grade = Grade.split('\n')[0]
                    if not Grade in HistogramData:
                        try:
                            Grade = GradeNames[int(Grade)]
                        except:
                            Grade = 'N'

                    if Factor is not None and Value is not None and Grade is not None:
                        try:
                            HistogramData[Grade].append(float(Factor) * float(Value))
                            NModules += 1
                        except:
                            print "Grade not defined: %s"%Grade
                    else:
                        self.ProblematicModulesList.append(RowTuple['ModuleID'])


        GradeAB = 1.e-6*float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
        GradeBC = 1.e-6*float(self.TestResultEnvironmentObject.GradingParameters['currentC'])

        HistogramOptions = {
            'GradeAB': GradeAB,
            'GradeBC': GradeBC,
            'TitleX': 'current [A]',
            'TitleY': '# modules',
            'TextSize': 0.02,
            'TextX1': 0.55,
            'TextY1': 0.67,
            'TextX2': 0.9,
            'TextY2': 0.82,
            'LogY': True,
            'LogX': True,
            'ShadeRegions': False,
        }
        self.DrawGradingRegionPlot(HistogramData, NBins, HistogramMin, HistogramMax, HistogramOptions)


        HTML = self.Image(self.Attributes['ImageFile'])
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)

