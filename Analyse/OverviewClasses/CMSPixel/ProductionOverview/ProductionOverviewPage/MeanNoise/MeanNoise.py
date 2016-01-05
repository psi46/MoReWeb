import ROOT
import AbstractClasses
import glob
import json

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='MeanNoiseROC'
        self.Name='CMSPixel_ProductionOverview_ProductionOverviewPage_%s'%self.NameSingle
        self.Title = 'MeanNoiseROC {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)

    def GenerateOverview(self):
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        NoiseMax = 600
        NBins = 120

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
                if RowTuple['TestType'] == self.Attributes['Test']:
                    for Chip in range(0, 16):
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'SCurveWidths', 'KeyValueDictPairs.json', 'mu', 'Value'])
                        try:
                            Grade = GradeNames[int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value']))]
                        except:
                            Grade = 'N'

                        if Value is not None and Grade is not None:
                            HistogramData[Grade].append(float(Value))
                            NROCs += 1

        HistogramOptions = {
            'GradeAB': float(self.TestResultEnvironmentObject.GradingParameters['noiseB']),
            'GradeBC': float(self.TestResultEnvironmentObject.GradingParameters['noiseC']),
            'TitleX': 'Noise [e-]',
            'TextSize': 0.02,
            'TextX1': 0.55,
            'TextY1': 0.67,
            'TextX2': 0.9,
            'TextY2': 0.82,
            'LogY': True,
        }
        self.DrawGradingRegionPlot(HistogramData, NBins, 0, NoiseMax, HistogramOptions)

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

        return self.Boxed(HTML)

