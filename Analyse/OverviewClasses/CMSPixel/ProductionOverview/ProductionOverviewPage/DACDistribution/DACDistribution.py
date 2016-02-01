# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses

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
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HistogramMin = self.Attributes['Minimum'] if 'Minimum' in self.Attributes else 0
        HistogramMax = self.Attributes['Maximum']
        NBins = self.Attributes['NBins']

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

        NROCs = 0
        for RowTuple in Rows:
            if RowTuple['ModuleID'] in ModuleIDsList:
                TestType = RowTuple['TestType']
                if TestType == self.Attributes['Test']:

                    for Chip in range(0, 16):
                        Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'DacParameterOverview', 'DacParameters{Trim}'.format(Trim=self.Attributes['Trim']), 'KeyValueDictPairs.json', self.Attributes['DAC'], 'Value'])
                        Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value'])

                        if Grade and '\n' in Grade:
                            Grade = Grade.split('\n')[0]
                        if not Grade in HistogramData:
                            try:
                                Grade = GradeNames[int(Grade)]
                            except:
                                Grade = 'N'

                        if Value is not None and Grade is not None and Grade in HistogramData:
                            HistogramData[Grade].append(float(Value))
                            NROCs += 1
                        else:
                            self.ProblematicModulesList.append(RowTuple['ModuleID'])

        HistogramOptions = {
            'GradeAB': None,
            'GradeBC': None,
            'TitleX': '{DAC} DAC Value'.format(DAC=self.Attributes['DAC']),
            'TextSize': 0.02,
            'TextX1': 0.15,
            'TextY1': 0.75,
            'TextX2': 0.45,
            'TextY2': 0.9,
            'LogY': True,
            'ShadeRegions': False,
        }
        self.DrawGradingRegionPlot(HistogramData, NBins, HistogramMin, HistogramMax, HistogramOptions)
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        return self.Boxed(HTML)

