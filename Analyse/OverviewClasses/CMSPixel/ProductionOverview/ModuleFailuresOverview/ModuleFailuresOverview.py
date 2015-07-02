# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='ModuleFailuresOverview'
    	self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Module Failures Overview'
        self.DisplayOptions = {
            'Width': 5,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1600, 600)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])


        ModuleIDsList.sort()
        YLabels = ['IVSlope', 'IV150', 'PedestalSpread', 'RelativeGainWidth', 'VcalThrWidth', 'Noise', 'BadROCs', 'AddressProblems', 'trimbitDefects', 'defectiveBumps', 'maskDefects', 'deadPixel', 'lowHREfficiency'][::-1]
        nGradings = 3*len(YLabels)
        Summary = ROOT.TH2D(self.GetUniqueID(), "", len(ModuleIDsList), 0, len(ModuleIDsList), nGradings, 0, nGradings)
        BinNumber = 1

        YBinNumber = 1
        for YLabel in YLabels:
            Summary.GetYaxis().SetBinLabel(YBinNumber, '')
            Summary.GetYaxis().SetBinLabel(YBinNumber+2, '')
            Summary.GetYaxis().SetBinLabel(YBinNumber+1, YLabel)
            YBinNumber += 3

        FullTests = ['m20_1','m20_2','p17_1'][::-1]

        ColorB = 0.84
        ColorC = 1.00

        for ModuleID in ModuleIDsList:

            Summary.GetXaxis().SetBinLabel(BinNumber, ModuleID)

            ### IV slope
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])
                        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['slopeivB'])
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'Variation', 'Value'])
                        if Value is not None and float(Value) > GradeAB:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IVSlope') + TestIndex, ColorB)

            ### IV 150
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
                        GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['currentC'])
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                        if Value is not None and float(Value) > GradeBC:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IV150') + TestIndex, ColorC)
                        elif Value is not None and float(Value) > GradeAB:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IV150') + TestIndex, ColorB)

            ### Pedestal Spread
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('PedestalSpread') + TestIndex, ColorC)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('PedestalSpread') + TestIndex, ColorB)

            ### RelativeGainWidth
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('RelativeGainWidth') + TestIndex, ColorC)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('RelativeGainWidth') + TestIndex, ColorB)

            ### VcalThrWidth
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('VcalThrWidth') + TestIndex, ColorC)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('VcalThrWidth') + TestIndex, ColorB)

            ### Noise
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('Noise') + TestIndex, ColorC)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('Noise') + TestIndex, ColorB)

            ### deadPixel
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('deadPixel') + TestIndex, ColorC)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('deadPixel') + TestIndex, ColorB)

            ### lowEfficiency
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] == 'XRayHRQualification':
                        TestIndex = 1

                        EfficiencyGrades = []
                        for Chip in range(0,16):
                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'EfficiencyGrade', 'Value'])
                            if Value is not None:
                                Grades = [grade for grade in Value.split('/') if grade.strip()[0] != '(']
                                EfficiencyGrades += Grades

                        if 'C' in EfficiencyGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('lowHREfficiency') + TestIndex, ColorC)
                        elif 'B' in EfficiencyGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('lowHREfficiency') + TestIndex, ColorB)

            BinNumber += 1

        Summary.Draw("col")
        line1 = ROOT.TLine()
        line1.SetLineStyle(2)
        linePositions = [3*i for i in range(1, len(YLabels))]

        for linePosition in linePositions:
            line1.DrawLine(0,linePosition,len(ModuleIDsList),linePosition)


        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)
        title.SetTextColor(self.GetGradeColor('B'))
        title.DrawText(0.15,0.965,"Grade B")

        title2 = ROOT.TText()
        title2.SetNDC()
        title2.SetTextAlign(12)
        title2.SetTextColor(self.GetGradeColor('C'))
        title2.DrawText(0.23,0.965,"Grade C")


        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

