import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle = 'DACSpreadPerModule'
        self.Name = 'CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = self.Attributes['Title']
        self.DisplayOptions = {
            'Width': 1,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(400, 400)

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(111210)
        ROOT.gPad.SetLogy(1)

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)

        HistogramMin = self.Attributes['HistogramMin'] # 0
        HistogramMax = self.Attributes['HistogramMax'] # 100
        NBins = self.Attributes['NBins'] #50

        GradeNames = {
            1: 'A',
            2: 'B',
            3: 'C',
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
                    Grade = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary1', 'KeyValueDictPairs.json', 'Grade', 'Value'])
                    JSONPath = [RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder']]
                    JSONPath += self.Attributes['JSONPath'] # ['CalDel', 'KeyValueDictPairs.json', "caldelspread", 'Value']
                    Value = self.GetJSONValue(JSONPath)

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
            'TitleX': self.Attributes['Title'],
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

        self.DisplayErrorsList()
        return self.Boxed(HTML)

