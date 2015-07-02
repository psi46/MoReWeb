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
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IVSlope') + TestIndex, 1)

            ### IV 150
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
                        GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['currentC'])
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                        if Value is not None and float(Value) > GradeBC:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IV150') + TestIndex, 2)
                        elif Value is not None and float(Value) > GradeAB:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IV150') + TestIndex, 1)

            ### Pedestal Spread
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('PedestalSpread') + TestIndex, 2)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('PedestalSpread') + TestIndex, 1)

            ### RelativeGainWidth
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('RelativeGainWidth') + TestIndex, 2)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('RelativeGainWidth') + TestIndex, 1)

            ### VcalThrWidth
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('VcalThrWidth') + TestIndex, 2)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('VcalThrWidth') + TestIndex, 1)

            ### Noise
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('Noise') + TestIndex, 2)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('Noise') + TestIndex, 1)

            ### deadPixel
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('deadPixel') + TestIndex, 2)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('deadPixel') + TestIndex, 1)

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
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('lowHREfficiency') + TestIndex, 2)
                        elif 'B' in EfficiencyGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('lowHREfficiency') + TestIndex, 1)

            BinNumber += 1



        Summary.Draw("colz")
        line1 = ROOT.TLine()
        line1.SetLineStyle(2)
        linePositions = [3*i for i in range(1, len(YLabels))]

        for linePosition in linePositions:
            line1.DrawLine(0,linePosition,len(ModuleIDsList),linePosition)



        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile'])

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

