import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.Name='CMSPixel_ProductionOverview_RelativeGainWidth'
        self.NameSingle='RelativeGainWidth'
        self.Title = 'RelativeGainWidth {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)


    def GenerateOverview(self):
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HistogramMax = 0.25
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
                TestType = RowTuple['TestType']

                if TestType == self.Attributes['Test']:

                    for Chip in range(0, 16):
                        Sigma = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'PHCalibrationGain', 'KeyValueDictPairs.json', 'sigma', 'Value'])
                        Mu = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'PHCalibrationGain', 'KeyValueDictPairs.json', 'mu', 'Value'])
                        try:
                            Grade = GradeNames[int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value']))]
                        except:
                            Grade = 'N'

                        if Sigma is not None and Mu is not None and float(Mu)>0 and Grade is not None:
                            HistogramData[Grade].append(float(Sigma) / float(Mu))
                            NROCs += 1

        HistogramOptions = {
            'GradeAB': float(self.TestResultEnvironmentObject.GradingParameters['gainB']),
            'GradeBC': float(self.TestResultEnvironmentObject.GradingParameters['gainC']),
            'TitleX': 'Rel. Gain Width [%]',
            'TextSize': 0.02,
            'TextX1': 0.55,
            'TextY1': 0.67,
            'TextX2': 0.9,
            'TextY2': 0.82,
            'LogY': True,
        }
        self.DrawGradingRegionPlot(HistogramData, NBins, 0, HistogramMax, HistogramOptions)

        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)
        return self.Boxed(HTML)

