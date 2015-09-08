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
        if self.Attributes.has_key('Width'):
            self.DisplayOptions['Width'] = self.Attributes['Width']
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1600, 500)
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
        YLabels = ['LCStartup', 'IVSlope', 'IV150', 'PedestalSpread', 'RelativeGainWidth', 'VcalThrWidth', 'Noise', 'TotalDefects', 'AddressDefects', 'trimbitDefects', 'BB_Fulltest', 'maskDefects', 'deadPixels', 'BB_X-ray', 'lowHREfficiency', 'ReadoutProblems', 'UniformityProblems', 'Noise_X-ray', 'TotalDefects_X-ray'][::-1]
        nGradings = 3*len(YLabels)
        Summary = ROOT.TH2D(self.GetUniqueID(), "", len(ModuleIDsList), 0, len(ModuleIDsList), nGradings, 0, nGradings)
        BinNumber = 1

        YBinNumber = 1
        for YLabel in YLabels:
            Summary.GetYaxis().SetBinLabel(YBinNumber, '')
            Summary.GetYaxis().SetBinLabel(YBinNumber+1, YLabel)
            Summary.GetYaxis().SetBinLabel(YBinNumber+2, '')
            YBinNumber += 3

        FullTests = ['m20_1','m20_2','p17_1'][::-1]
        TestTypeLeakageCurrentPON = ['LeakageCurrentPON']
        TestTypeXrayHR = 'XRayHRQualification'

        ColorB = 0.84
        ColorC = 1.00

        GradePixelDefectsAB = float(self.TestResultEnvironmentObject.GradingParameters['defectsB'])
        GradePixelDefectsBC = float(self.TestResultEnvironmentObject.GradingParameters['defectsC'])

        GradeMaskDefectsAB = float(self.TestResultEnvironmentObject.GradingParameters['maskDefectsB'])
        GradeMaskDefectsBC = float(self.TestResultEnvironmentObject.GradingParameters['maskDefectsC'])

        for ModuleID in ModuleIDsList:

            Summary.GetXaxis().SetBinLabel(BinNumber, ModuleID)

            ### LeakageCurrent PON
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in TestTypeLeakageCurrentPON:
                        GradeC = 15*1e-6
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'KeyValueDictPairs.json', 'LeakageCurrent', 'Value'])
                        if Value is not None and float(Value) > GradeC:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('LCStartup') + i, ColorC)

            ### IV slope
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])
                        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['slopeivB'])
                        GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['slopeivC'])
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'Variation', 'Value'])
                        if Value is not None and float(Value) > GradeBC:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IVSlope') + TestIndex, ColorC)
                        elif Value is not None and float(Value) > GradeAB:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('IVSlope') + TestIndex, ColorB)

            ### IV 150
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        if not RowTuple['Temperature'] or int(RowTuple['Temperature']) == 17:
                            #  grading criteria for measured currents
                            GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
                            GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['currentC'])
                        else:
                            # grading criteria for recalculated currents
                            GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['currentBm10'])
                            GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['currentCm10'])

                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary3', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
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
                        RocGrades = []
                        for Chip in range(0,16):
                            NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'PixelMap', 'KeyValueDictPairs.json', 'NDeadPixels', 'Value'])
                            if NDefects:
                                NDefects = int(NDefects)
                                if NDefects >= GradePixelDefectsBC:
                                    RocGrades.append('C')
                                elif  NDefects >= GradePixelDefectsAB:
                                    RocGrades.append('B')
                        if 'C' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('deadPixels') + TestIndex, ColorC)
                        elif 'B' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('deadPixels') + TestIndex, ColorB)

            ### AddressDefects
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])
                        RocGrades = []
                        for Chip in range(0,16):
                            NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'AddressDecoding', 'KeyValueDictPairs.json', 'NAddressDecodingProblems', 'Value'])
                            if NDefects:
                                NDefects = int(NDefects)
                                if NDefects >= GradePixelDefectsBC:
                                    RocGrades.append('C')
                                elif  NDefects >= GradePixelDefectsAB:
                                    RocGrades.append('B')
                        if 'C' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('AddressDefects') + TestIndex, ColorC)
                        elif 'B' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('AddressDefects') + TestIndex, ColorB)

            ### maskDefects
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])
                        RocGrades = []
                        for Chip in range(0,16):
                            NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'PixelMap', 'KeyValueDictPairs.json', 'NMaskDefects', 'Value'])
                            if NDefects:
                                NDefects = int(NDefects)
                                if NDefects >= GradeMaskDefectsBC:
                                    RocGrades.append('C')
                                elif  NDefects >= GradeMaskDefectsAB:
                                    RocGrades.append('B')
                        if 'C' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('maskDefects') + TestIndex, ColorC)
                        elif 'B' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('maskDefects') + TestIndex, ColorB)

            ### trimbitDefects
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])
                        RocGrades = []
                        for Chip in range(0,16):
                            NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'TrimBitProblems', 'KeyValueDictPairs.json', 'nDeadTrimbits', 'Value'])
                            if NDefects:
                                NDefects = int(NDefects)
                                if NDefects >= GradePixelDefectsBC:
                                    RocGrades.append('C')
                                elif  NDefects >= GradePixelDefectsAB:
                                    RocGrades.append('B')
                        if 'C' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('trimbitDefects') + TestIndex, ColorC)
                        elif 'B' in RocGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('trimbitDefects') + TestIndex, ColorB)

            ### TotalDefects
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsRocsB', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsRocsC', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('TotalDefects') + TestIndex, ColorC)
                        elif ValueB is not None and float(ValueB) > 0:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('TotalDefects') + TestIndex, ColorB)

            ### defectiveBumps Fulltest
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])
                        BBGrades = []
                        for Chip in range(0,16):
                            NDefectiveBumps = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'BumpBonding', 'KeyValueDictPairs.json', 'nBumpBondingProblems', 'Value'])
                            if NDefectiveBumps:
                                NDefectiveBumps = int(NDefectiveBumps)
                                if NDefectiveBumps >= GradePixelDefectsBC:
                                    BBGrades.append('C')
                                elif  NDefectiveBumps >= GradePixelDefectsAB:
                                    BBGrades.append('B')
                        if 'C' in BBGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('BB_Fulltest') + TestIndex, ColorC)
                        elif 'B' in BBGrades:
                            Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('BB_Fulltest') + TestIndex, ColorB)

            ### defectiveBumps X-ray
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        BBGrades = []
                        for Chip in range(0,16):
                            BBGradesROC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'HitMapGrade', 'Value'])
                            if BBGradesROC:
                                for BBGradeROC in BBGradesROC.split("/"):
                                    if not '(' in BBGradeROC and len(BBGradeROC)>0:
                                        BBGrades.append(BBGradeROC)

                        if 'C' in BBGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('BB_X-ray') + i, ColorC)
                        elif 'B' in BBGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('BB_X-ray') + i, ColorB)

            ### lowEfficiency
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        EfficiencyGrades = []
                        for Chip in range(0,16):
                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'EfficiencyGrade', 'Value'])
                            if Value is not None:
                                Grades = [grade for grade in Value.split('/') if grade.strip()[0] != '(']
                                EfficiencyGrades += Grades

                        if 'C' in EfficiencyGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('lowHREfficiency') + i, ColorC)
                        elif 'B' in EfficiencyGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('lowHREfficiency') + i, ColorB)

            ### r/o problems
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ROCsWithReadoutProblems', 'Value'])
                        if Value is not None and Value > 0:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('ReadoutProblems') + i, ColorC)

            ### unif problems
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ROCsWithUniformityProblems', 'Value'])
                        if Value is not None and Value > 0:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('UniformityProblems') + i, ColorC)

            ### X-ray noise
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        RocGrades = []
                        for Chip in range(0,16):
                            # pixel
                            NDefects = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'HiddenData.json', 'NoiseDefects', 'Value'])
                            if NDefects:
                                NDefects = int(NDefects)
                                if NDefects >= GradePixelDefectsBC:
                                    RocGrades.append('C')
                                elif  NDefects >= GradePixelDefectsAB:
                                    RocGrades.append('B')
                            # mean
                            MeanNoiseGrade = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'NoiseGrade', 'Value'])
                            if MeanNoiseGrade:
                                RocGrades.append(MeanNoiseGrade)

                        if 'C' in RocGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('Noise_X-ray') + i, ColorC)
                        elif 'B' in RocGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('Noise_X-ray') + i, ColorB)

            ### totalDefects X-ray
            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    if RowTuple['TestType'] == TestTypeXrayHR:
                        RocGrades = []
                        for Chip in range(0,16):
                            NDefects = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                            if NDefects:
                                NDefects = int(NDefects)
                                if NDefects >= GradePixelDefectsBC:
                                    RocGrades.append('C')
                                elif  NDefects >= GradePixelDefectsAB:
                                    RocGrades.append('B')

                        if 'C' in RocGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('TotalDefects_X-ray') + i, ColorC)
                        elif 'B' in RocGrades:
                            for i in range(3):
                                Summary.SetBinContent(BinNumber, 1 + 3*YLabels.index('TotalDefects_X-ray') + i, ColorB)

            BinNumber += 1

        ROOT.gPad.SetLeftMargin(0.16)
        ROOT.gPad.SetRightMargin(0.03)

        Summary.Draw("col")
        Summary.GetZaxis().SetRangeUser(0, 1.0)
        Summary.GetYaxis().SetLabelSize(0.055)


        Summary.GetXaxis().LabelsOption("v")
        if len(ModuleIDsList) > 200:
            Summary.GetXaxis().SetLabelSize(0.015)
        elif len(ModuleIDsList) > 100:
            Summary.GetXaxis().SetLabelSize(0.025)
        elif len(ModuleIDsList) > 50:
            Summary.GetXaxis().SetLabelSize(0.035)
        else:
            Summary.GetXaxis().SetLabelSize(0.05)

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
        HTML = self.Image(self.Attributes['ImageFile'], {'height': '350px'})

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

