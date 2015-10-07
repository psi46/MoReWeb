# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import time
import glob

class ModuleSummaryValues(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def MakeArray(self):

        
        Numbers = {
        'nA' : 0,
        'nB' : 0,
        'nC' : 0,
        'nM' : 0,
        'nlcstartupB': 0, 
        'nlcstartupC' : 0,
        'nIV150B' : 0,
        'nIV150C' : 0,
        'nIVSlopeB' : 0,
        'nIVSlopeC' : 0,
        'nRecCurrentB' : 0,
        'nRecCurrentC' : 0,
        'nCurrentRatioB' : 0,
        'nCurrentRatioC' : 0,
        'ntotDefectsB' : 0,
        'ntotDefectsC' : 0,
        'ntotDefectsXrayB' : 0,
        'ntotDefectsXrayC' : 0,
        'nBBFullB' : 0,
        'nBBFullC' : 0,
        'nBBXrayB' : 0,
        'nBBXrayC' : 0,
        'nAddressdefB' : 0,
        'nAddressdefC' : 0,
        'nTrimbitdefB' : 0,
        'nTrimbitdefC' : 0,
        'nMaskdefB' : 0,
        'nMaskdefC' : 0,
        'ndeadpixB' : 0,
        'ndeadpixC' : 0,
        'nuniformityB' : 0,
        'nuniformityC' : 0,
        'nNoiseB' : 0,
        'nNoiseC' : 0,
        'nNoiseXrayB' : 0,
        'nNoiseXrayC' : 0,
        'nPedSpreadB' : 0,
        'nPedSpreadC' : 0,
        'nRelGainWB' : 0,
        'nRelGainWC' : 0,
        'nVcalThrWB' : 0,
        'nVcalThrWC' : 0,
        'nLowHREfB' : 0,
        'nLowHREfC' : 0
        }

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])
        ModuleIDsList.sort(reverse=True)

        FullTests = ['m20_1','m20_2','p17_1'][::-1]
        TestTypeLeakageCurrentPON = ['LeakageCurrentPON']
        TestTypeXrayHR = 'XRayHRQualification'
        Final_Grades = []

        FTMinus20BTC_Grades = []
        FTMinus20ATC_Grades = []
        FT17_Grades = []
        XrayCal_Grades = []
        XrayHR_Grades = []
        Final_Grades = []

        for ModuleID in ModuleIDsList:

            FTMinus20BTC = ''
            FTMinus20ATC = ''
            FT17 = ''
            XrayCal = ''
            XrayHR = ''
            Complete = ''

            ModuleGrades = []

            for RowTuple in Rows:
                if RowTuple['ModuleID']==ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == 'm20_1':
                        FTMinus20BTC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'm20_2':
                        FTMinus20ATC = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'p17_1':
                        FT17 =  RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XrayCalibration_Spectrum':
                        XrayCal = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])
                    if TestType == 'XRayHRQualification':
                        XrayHR = RowTuple['Grade'] if RowTuple['Grade'] is not None else ''
                        ModuleGrades.append(RowTuple['Grade'])


            if self.ModuleQualificationIsComplete(ModuleID, Rows):
                FinalGrade = self.GetFinalGrade(ModuleID, Rows)
                Final_Grades.append(FinalGrade)
        

        Numbers['nA'] = len([x for x in Final_Grades if x=='A'])
        Numbers['nB'] = len([x for x in Final_Grades if x=='B'])
        Numbers['nC'] = len([x for x in Final_Grades if x=='C'])

        #missing = len(ModuleIDsList) - len(Final_Grades)

        Numbers['nM'] = len(ModuleIDsList) - len(Final_Grades)
        
        GradePixelDefectsAB = float(self.TestResultEnvironmentObject.GradingParameters['defectsB'])
        GradePixelDefectsBC = float(self.TestResultEnvironmentObject.GradingParameters['defectsC'])

        GradeMaskDefectsAB = float(self.TestResultEnvironmentObject.GradingParameters['maskDefectsB'])
        GradeMaskDefectsBC = float(self.TestResultEnvironmentObject.GradingParameters['maskDefectsC'])


        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    
            ### LeakageCurrent PON
                    if RowTuple['TestType'] in TestTypeLeakageCurrentPON:
                        GradeC = 15*1e-6
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'KeyValueDictPairs.json', 'LeakageCurrent', 'Value'])
                        if Value is not None and float(Value) > GradeC:
                            Numbers['nlcstartupC'] += 1
                            break
                            
            ### IV slope
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])
                        GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['slopeivB'])
                        GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['slopeivC'])

                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'Variation', 'Value'])
                        if Value is not None and float(Value) > GradeBC:
                            Numbers['nIVSlopeC'] += 1
                            break
                        elif Value is not None and float(Value) > GradeAB:
                            Numbers['nIVSlopeB'] += 1
                            break

            ### IV 150 & leakage curent ratio
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        if not RowTuple['Temperature'] or int(RowTuple['Temperature']) == 17:
                            #  grading criteria for measured currents
                            GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
                            GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['currentC'])

                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary3', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                            if Value is not None and float(Value) > GradeBC:
                                Numbers['nIV150C'] += 1
                            elif Value is not None and float(Value) > GradeAB:
                                Numbers['nIV150B'] += 1
                        elif int(RowTuple['Temperature']) == -20:
                            GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['leakageCurrentRatioB'])
                            GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['leakageCurrentRatioC'])

                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentRatio150V', 'Value'])
                            if Value is not None and float(Value) < GradeBC:
                                Numbers['nCurrentRatioC'] += 1
                            elif Value is not None and float(Value) < GradeAB:
                                Numbers['nCurrentRatioB'] += 1


            ### Pedestal Spread
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Numbers['nPedSpreadC'] += 1
                            break
                        elif ValueB is not None and float(ValueB) > 0:
                            Numbers['nPedSpreadB'] += 1
                            break

            ### RelativeGainWidth
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Numbers['nRelGainWC'] += 1
                            break
                        elif ValueB is not None and float(ValueB) > 0:
                            Numbers['nRelGainWB'] += 1
                            break

            ### VcalThrWidth
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Numbers['nVcalThrWC'] += 1
                            break
                        elif ValueB is not None and float(ValueB) > 0:
                            Numbers['nVcalThrWB'] += 1
                            break

            ### Noise
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeBROCs', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeCROCs', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Numbers['nNoiseC'] += 1
                            break
                        elif ValueB is not None and float(ValueB) > 0:
                            Numbers['nNoiseB'] += 1
                            break

            ### deadPixel
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
                            Numbers['ndeadpixC'] += 1
                            break
                        elif 'B' in RocGrades:
                            Numbers['ndeadpixB'] += 1
                            break

            ### AddressDefects
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
                            Numbers['nAddressdefC'] += 1
                            break
                        elif 'B' in RocGrades:
                            Numbers['nAddressdefB'] += 1
                            break

            ### maskDefects
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
                            Numbers['nMaskdefC'] += 1
                            break
                        elif 'B' in RocGrades:
                            Numbers['nMaskdefB'] += 1
                            break

            ### trimbitDefects
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
                            Numbers['nTrimbitdefC'] += 1
                            break
                        elif 'B' in RocGrades:
                            Numbers['nTrimbitdefB'] += 1
                            break

            ### TotalDefects
                    if RowTuple['TestType'] in FullTests:
                        TestIndex = FullTests.index(RowTuple['TestType'])

                        ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsRocsB', 'Value'])
                        ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsRocsC', 'Value'])

                        if ValueC is not None and float(ValueC) > 0:
                            Numbers['ntotDefectsC'] += 1
                            break
                        elif ValueB is not None and float(ValueB) > 0:
                            Numbers['ntotDefectsB'] += 1
                            break

            ### defectiveBumps Fulltest
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
                            Numbers['nBBFullC'] += 1
                            break
                        elif 'B' in BBGrades:
                            Numbers['nBBFullB'] += 1
                            break

            ### defectiveBumps X-ray
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        BBGrades = []
                        for Chip in range(0,16):
                            BBGradesROC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'HitMapGrade', 'Value'])
                            if BBGradesROC:
                                for BBGradeROC in BBGradesROC.split("/"):
                                    if not '(' in BBGradeROC and len(BBGradeROC)>0:
                                        BBGrades.append(BBGradeROC)

                        if 'C' in BBGrades:
                            Numbers['nBBXrayC'] += 1
                            break
                        elif 'B' in BBGrades:
                            Numbers['nBBXrayB'] += 1
                            break

            ### lowEfficiency
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        EfficiencyGrades = []
                        for Chip in range(0,16):
                            Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'EfficiencyGrade', 'Value'])
                            if Value is not None:
                                Grades = [grade for grade in Value.split('/') if grade.strip()[0] != '(']
                                EfficiencyGrades += Grades

                        if 'C' in EfficiencyGrades:
                                Numbers['nLowHREfC'] += 1
                                break
                        elif 'B' in EfficiencyGrades:
                                Numbers['nLowHREfB'] += 1 
                                break       

            ### unif problems
                    if RowTuple['TestType'] == TestTypeXrayHR:

                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ROCsWithUniformityProblems', 'Value'])
                        if Value is not None and Value > 0:
                                Numbers['nuniformityC'] += 1
                                break

            ### X-ray noise
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
                            Numbers['nNoiseXrayC'] += 1
                            break
                        elif 'B' in RocGrades:
                            Numbers['nNoiseXrayB'] += 1
                            break

            ### totalDefects X-ray
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
                            Numbers['ntotDefectsXrayC'] += 1
                            break
                        elif 'B' in RocGrades:
                            Numbers['ntotDefectsXrayB'] += 1
                            break


        return Numbers


