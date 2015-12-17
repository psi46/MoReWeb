import ROOT
import AbstractClasses

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
        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HistogramMin = 90
        HistogramMax = 102
        NBins = 100
        
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
                if TestType == 'XRayHRQualification':
                    for Chip in range(0, 16):
                        Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip,  'EfficiencyInterpolation', 'KeyValueDictPairs.json', "InterpolatedEfficiency{Rate}".format(Rate=self.Attributes['Rate']), 'Value'])
                        Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','ROCGrade','Value'])
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
            'GradeAB': float(self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_Rate2']),
            'GradeBC': float(self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_Rate2']),
            'TitleX': 'Efficiency',
            'TextSize': 0.02,
            'TextX1': 0.15,
            'TextY1': 0.75,
            'TextX2': 0.45,
            'TextY2': 0.9,
            'LogY': True,
        }
        self.DrawGradingRegionPlot(HistogramData, NBins, HistogramMin, HistogramMax, HistogramOptions)
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of ROCs: %d"%NROCs)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        ROOT.gPad.SetLogx(0)
        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)


