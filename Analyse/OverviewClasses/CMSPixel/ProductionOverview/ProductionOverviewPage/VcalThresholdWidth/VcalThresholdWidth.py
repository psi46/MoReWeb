import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):

        self.NameSingle='VcalThresholdWidth'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Vcal Thr. Width {Test}'.format(Test=self.Attributes['Test'])
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)


    def GenerateOverview(self):
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)


        HistogramMax = 600
        NBins = 120
        ScaleFactor = self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']

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
                        Sigma = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip, 'VcalThresholdTrimmed', 'KeyValueDictPairs.json', 'sigma', 'Value'])
                        try:
                            Grade = GradeNames[int(self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','PixelDefectsGrade','Value']))]
                        except:
                            Grade = 'N'

                        if Sigma is not None and Grade is not None:
                            HistogramData[Grade].append(ScaleFactor * float(Sigma))
                            NROCs += 1

        HistogramOptions = {
            'GradeAB': float(self.TestResultEnvironmentObject.GradingParameters['trimmingB']),
            'GradeBC': float(self.TestResultEnvironmentObject.GradingParameters['trimmingC']),
            'TitleX': 'Threshold Width [e-]',
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

        ROOT.gPad.SetLogx(0)
        ROOT.gPad.SetLogy(0)
        return self.Boxed(HTML)

