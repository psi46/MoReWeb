import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='VcalSlope'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Vcal Slope'
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400,500)

    def GenerateOverview(self):

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HistogramMin = 30
        HistogramMax = 64
        NBins = 68

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

                if TestType == 'XrayCalibration_Spectrum':
                    for Chip in range(0, 16):
                        Value = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips_Xray', 'Chip_Xray%d'%Chip,  'Xray_Calibration_Spectrum_Chip%d'%Chip, 'KeyValueDictPairs.json', "Slope", 'Value'])
                        Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'],'QualificationGroup','XRayHRQualification','Chips','Chip%d'%Chip,'Grading','KeyValueDictPairs.json','ROCGrade','Value'])

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
            'TitleX': 'e^-/Vcal[DAC]',
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

        ROOT.gPad.SetLogx(0)
        ROOT.gPad.SetLogy(0)
        self.DisplayErrorsList()
        return self.Boxed(HTML)


