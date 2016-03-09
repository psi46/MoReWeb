# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob
import sys
import time
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser
import json

from AbstractClasses.Helper.SetEncoder import SetEncoder

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='ModuleFailuresOverview'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Module Failures Overview'
        self.DisplayOptions = {
            'Width': 5.4,
        }
        if self.Attributes.has_key('Width'):
            self.DisplayOptions['Width'] = self.Attributes['Width']
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1600, 500)
        self.Canvas.SetFrameLineStyle(0)
        self.Canvas.SetFrameLineWidth(1)
        self.Canvas.SetFrameBorderMode(0)
        self.Canvas.SetFrameBorderSize(1)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)

        NumModules = int(self.Attributes['NumModules']) if 'NumModules' in self.Attributes else 9999
        Offset = int(self.Attributes['Offset']) if 'Offset' in self.Attributes else 0

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows, NumModules, Offset)
        try:
            self.Title = 'Module Failures Overview: %s to %s'%(ModuleIDsList[0], ModuleIDsList[-1])
        except:
            pass

        YLabels = ['LCStartup', 'IVSlope', 'IV150', 'IVRatio150', 'GradeFT', 'ManualGradeFT', 'DeadROC', 'PedestalSpread', 'RelativeGainWidth', 'VcalThrWidth', 'Noise', 'TotalDefects', 'AddressDefects', 'trimbitDefects', 'BB_Fulltest', 'maskDefects', 'deadPixels', 'GradeHR', 'ManualGradeHR', 'BB_X-ray', 'lowHREfficiency', 'DoubleColumn', 'ReadoutProblems', 'UniformityProblems', 'Noise_X-ray', 'TotalDefects_X-ray'][::-1]
        nGradings = 3*len(YLabels)
        Summary = ROOT.TH2D(self.GetUniqueID(), "", len(ModuleIDsList), 0, len(ModuleIDsList), nGradings, 0, nGradings)
        Summary.GetYaxis().SetTickLength(0)

        YBinNumber = 1
        for YLabel in YLabels:
            Summary.GetYaxis().SetBinLabel(YBinNumber, '')
            Summary.GetYaxis().SetBinLabel(YBinNumber+1, YLabel)
            Summary.GetYaxis().SetBinLabel(YBinNumber+2, '')
            YBinNumber += 3

        FullTests = ['m20_1','m20_2','p17_1'][::-1]
        TestTypeLeakageCurrentPON = ['LeakageCurrentPON']
        TestTypeXrayHR = 'XRayHRQualification'

        ColorA = 0.5
        ColorB = 0.84
        ColorC = 1.00

        GradePixelDefectsAB = float(self.TestResultEnvironmentObject.GradingParameters['defectsB'])
        GradePixelDefectsBC = float(self.TestResultEnvironmentObject.GradingParameters['defectsC'])

        GradeMaskDefectsAB = float(self.TestResultEnvironmentObject.GradingParameters['maskDefectsB'])
        GradeMaskDefectsBC = float(self.TestResultEnvironmentObject.GradingParameters['maskDefectsC'])

        DefectsDict = {}

        for ModuleID in ModuleIDsList:
            # initialize defects dictionary
            DefectsDict[ModuleID] = {}
            for DefectCategory in YLabels:
                DefectsDict[ModuleID][DefectCategory] = {}

        ModulesCount = 0
        ModulesProgressPercentOld = 0
        nRows = len(Rows)
        for RowTuple in Rows:
            ModulesProgressPercent = int(float(100.0 * ModulesCount / nRows))
            if ModulesProgressPercent != ModulesProgressPercentOld:
                ModulesProgressPercentOld = ModulesProgressPercent
                sys.stdout.write('%d%% '%ModulesProgressPercent)
            ModulesCount = ModulesCount + 1
            sys.stdout.flush()

            ModuleID = RowTuple['ModuleID']

            if ModuleID in ModuleIDsList:

        ### LeakageCurrent PON
                if RowTuple['TestType'] in TestTypeLeakageCurrentPON:
                    GradeC = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_C']*1e-6
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'KeyValueDictPairs.json', 'LeakageCurrent', 'Value'])
                    if Value is not None and float(Value) > GradeC:
                        DefectsDict[ModuleID]['LCStartup'] = 'C'
                    elif Value is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### IV slope
                if RowTuple['TestType'] in FullTests and (not RowTuple['Temperature'] or (len(RowTuple['Temperature'].strip()) > 0 and int(RowTuple['Temperature']) == 17)):
                    TestIndex = FullTests.index(RowTuple['TestType'])
                    GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['slopeivB'])
                    GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['slopeivC'])
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'Variation', 'Value'])
                    if Value is not None and float(Value) > GradeBC:
                        DefectsDict[ModuleID]['IVSlope'] = 'C'
                    elif Value is not None and float(Value) > GradeAB:
                        DefectsDict[ModuleID]['IVSlope'] = 'B'
                    elif Value is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### IV ratio 150
                if RowTuple['TestType'] in FullTests and (RowTuple['Temperature'] and int(RowTuple['Temperature']) == -20):
                    TestIndex = FullTests.index(RowTuple['TestType'])
                    GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['leakageCurrentRatioB'])
                    GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['leakageCurrentRatioC'])

                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentRatio150V', 'Value'])
                    if Value is not None and float(Value) < GradeBC:
                        DefectsDict[ModuleID]['IVRatio150'][RowTuple['TestType']] = 'C'
                    elif Value is not None and float(Value) < GradeAB:
                        DefectsDict[ModuleID]['IVRatio150'][RowTuple['TestType']] = 'B'
                    elif Value is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### IV 150
                if RowTuple['TestType'] in FullTests:
                    TestIndex = FullTests.index(RowTuple['TestType'])

                    #  grading criteria for measured currents
                    GradeAB = float(self.TestResultEnvironmentObject.GradingParameters['currentB'])
                    GradeBC = float(self.TestResultEnvironmentObject.GradingParameters['currentC'])

                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'IVCurve', 'KeyValueDictPairs.json', 'CurrentAtVoltage150V', 'Value'])
                    if Value is not None and float(Value) > GradeBC:
                        DefectsDict[ModuleID]['IV150'][RowTuple['TestType']] = 'C'
                    elif Value is not None and float(Value) > GradeAB:
                        DefectsDict[ModuleID]['IV150'][RowTuple['TestType']] = 'B'
                    elif Value is None:
                        self.ProblematicModulesList.append(ModuleID)

                if RowTuple['TestType'] in FullTests:
                    TestIndex = FullTests.index(RowTuple['TestType'])

        ### GradeFT
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ModuleGrade', 'Value'])
                    if Value is not None:
                        try:
                            Value = int(Value)
                            if Value == 3:
                                DefectsDict[ModuleID]['GradeFT'][RowTuple['TestType']] = 'C'
                            elif Value == 2:
                                DefectsDict[ModuleID]['GradeFT'][RowTuple['TestType']] = 'B'
                        except:
                            self.ProblematicModulesList.append(ModuleID)
        ### DEFECTS for defects.txt
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Summary1', 'KeyValueDictPairs.json', 'SpecialDefects', 'Value'])
                    if Value is not None:
                        try:
                            DefectsList = [x.strip() for x in Value.split(',')]
                            for Defect in DefectsList:
                                if 'DEFECT_%s'%Defect not in DefectsDict[ModuleID]:
                                    DefectsDict[ModuleID]['DEFECT_%s'%Defect] = {}
                                DefectsDict[ModuleID]['DEFECT_%s'%Defect][RowTuple['TestType']] = 'C'
                        except:
                            self.ProblematicModulesList.append(ModuleID)

        ### ManualGradeFT
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ManualGrade', 'Value'])
                    if Value is not None:
                        try:
                            GradeNames = ['A', 'B', 'C']
                            if Value in GradeNames:
                                Value = 1 + GradeNames.index(Value)
                            else:
                                Value = int(Value)
                            if Value == 3:
                                DefectsDict[ModuleID]['ManualGradeFT'][RowTuple['TestType']] = 'C'
                            elif Value == 2:
                                DefectsDict[ModuleID]['ManualGradeFT'][RowTuple['TestType']] = 'B'
                            elif Value == 1:
                                # also list grade A here because it can negate effect of other defects!
                                DefectsDict[ModuleID]['ManualGradeFT'][RowTuple['TestType']] = 'A'
                        except:
                            self.ProblematicModulesList.append(ModuleID)

        ### DeadROC
                    DeadROCs = 0
                    for Chip in range(0,16):
                        NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Summary', 'KeyValueDictPairs.json', 'Total', 'Value'])
                        if NDefects:
                            try:
                                NDefects = int(NDefects)
                                if NDefects > 3999:
                                    DeadROCs +=1
                            except:
                                self.ProblematicModulesList.append(ModuleID)

                    if DeadROCs > 0:
                        DefectsDict[ModuleID]['DeadROC'][RowTuple['TestType']] = 'C'


        ### Pedestal Spread
                    ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeBROCs', 'Value'])
                    ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PedestalSpreadGradeCROCs', 'Value'])

                    if ValueC is not None and float(ValueC) > 0:
                        DefectsDict[ModuleID]['PedestalSpread'][RowTuple['TestType']] = 'C'
                    elif ValueB is not None and float(ValueB) > 0:
                        DefectsDict[ModuleID]['PedestalSpread'][RowTuple['TestType']] = 'B'
                    elif ValueB is None or ValueC is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### RelativeGainWidth
                    ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeBROCs', 'Value'])
                    ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'RelativeGainWidthGradeCROCs', 'Value'])

                    if ValueC is not None and float(ValueC) > 0:
                        DefectsDict[ModuleID]['RelativeGainWidth'][RowTuple['TestType']] = 'C'
                    elif ValueB is not None and float(ValueB) > 0:
                        DefectsDict[ModuleID]['RelativeGainWidth'][RowTuple['TestType']] = 'B'
                    elif ValueB is None or ValueC is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### VcalThrWidth
                    ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeBROCs', 'Value'])
                    ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'VcalThresholdWidthGradeCROCs', 'Value'])

                    if ValueC is not None and float(ValueC) > 0:
                        DefectsDict[ModuleID]['VcalThrWidth'][RowTuple['TestType']] = 'C'
                    elif ValueB is not None and float(ValueB) > 0:
                        DefectsDict[ModuleID]['VcalThrWidth'][RowTuple['TestType']] = 'B'
                    elif ValueB is None or ValueC is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### Noise
                    ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeBROCs', 'Value'])
                    ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'NoiseGradeCROCs', 'Value'])

                    if ValueC is not None and float(ValueC) > 0:
                        DefectsDict[ModuleID]['Noise'][RowTuple['TestType']] = 'C'
                    elif ValueB is not None and float(ValueB) > 0:
                        DefectsDict[ModuleID]['Noise'][RowTuple['TestType']] = 'B'
                    elif ValueB is None or ValueC is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### deadPixel
                    RocGrades = []
                    for Chip in range(0,16):
                        NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'PixelMap', 'KeyValueDictPairs.json', 'NDeadPixels', 'Value'])
                        if NDefects:
                            NDefects = int(NDefects)
                            if NDefects >= GradePixelDefectsBC:
                                RocGrades.append('C')
                            elif  NDefects >= GradePixelDefectsAB:
                                RocGrades.append('B')
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                    if 'C' in RocGrades:
                        DefectsDict[ModuleID]['deadPixels'][RowTuple['TestType']] = 'C'
                    elif 'B' in RocGrades:
                        DefectsDict[ModuleID]['deadPixels'][RowTuple['TestType']] = 'B'


        ### AddressDefects
                    RocGrades = []
                    for Chip in range(0,16):
                        NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'AddressDecoding', 'KeyValueDictPairs.json', 'NAddressDecodingProblems', 'Value'])
                        if NDefects:
                            NDefects = int(NDefects)
                            if NDefects >= GradePixelDefectsBC:
                                RocGrades.append('C')
                            elif  NDefects >= GradePixelDefectsAB:
                                RocGrades.append('B')
                        else:
                            self.ProblematicModulesList.append(ModuleID)

                    if 'C' in RocGrades:
                        DefectsDict[ModuleID]['AddressDefects'][RowTuple['TestType']] = 'C'
                    elif 'B' in RocGrades:
                        DefectsDict[ModuleID]['AddressDefects'][RowTuple['TestType']] = 'B'

        ### maskDefects
                    RocGrades = []
                    for Chip in range(0,16):
                        NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'PixelMap', 'KeyValueDictPairs.json', 'NMaskDefects', 'Value'])
                        if NDefects:
                            NDefects = int(NDefects)
                            if NDefects >= GradeMaskDefectsBC:
                                RocGrades.append('C')
                            elif  NDefects >= GradeMaskDefectsAB:
                                RocGrades.append('B')
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                    if 'C' in RocGrades:
                        DefectsDict[ModuleID]['maskDefects'][RowTuple['TestType']] = 'C'
                    elif 'B' in RocGrades:
                        DefectsDict[ModuleID]['maskDefects'][RowTuple['TestType']] = 'B'

        ### trimbitDefects
                    RocGrades = []
                    for Chip in range(0,16):
                        NDefects = self.GetJSONValue([RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'TrimBitProblems', 'KeyValueDictPairs.json', 'nDeadTrimbits', 'Value'])
                        if NDefects:
                            NDefects = int(NDefects)
                            if NDefects >= GradePixelDefectsBC:
                                RocGrades.append('C')
                            elif  NDefects >= GradePixelDefectsAB:
                                RocGrades.append('B')
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                    if 'C' in RocGrades:
                        DefectsDict[ModuleID]['trimbitDefects'][RowTuple['TestType']] = 'C'
                    elif 'B' in RocGrades:
                        DefectsDict[ModuleID]['trimbitDefects'][RowTuple['TestType']] = 'B'

        ### TotalDefects
                    ValueB = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsRocsB', 'Value'])
                    ValueC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'PixelDefectsRocsC', 'Value'])

                    if ValueC is not None and float(ValueC) > 0:
                        DefectsDict[ModuleID]['TotalDefects'][RowTuple['TestType']] = 'C'
                    elif ValueB is not None and float(ValueB) > 0:
                        DefectsDict[ModuleID]['TotalDefects'][RowTuple['TestType']] = 'B'
                    elif ValueB is None or ValueC is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### defectiveBumps Fulltest
                    BBGrades = []
                    for Chip in range(0,16):
                        NDefectiveBumps = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'BumpBonding', 'KeyValueDictPairs.json', 'nBumpBondingProblems', 'Value'])
                        if NDefectiveBumps:
                            NDefectiveBumps = int(NDefectiveBumps)
                            if NDefectiveBumps >= GradePixelDefectsBC:
                                BBGrades.append('C')
                            elif  NDefectiveBumps >= GradePixelDefectsAB:
                                BBGrades.append('B')
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                    if 'C' in BBGrades:
                        DefectsDict[ModuleID]['BB_Fulltest'][RowTuple['TestType']] = 'C'
                    elif 'B' in BBGrades:
                        DefectsDict[ModuleID]['BB_Fulltest'][RowTuple['TestType']] = 'B'

### HIGH RATE TESTS

                if RowTuple['TestType'] == TestTypeXrayHR:

        ### GradeHR
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ModuleGrade', 'Value'])
                    if Value is not None:
                        GradeNames = ['A', 'B', 'C']
                        if Value in GradeNames:
                            Value = 1 + GradeNames.index(Value)
                        try:                            
                            GradeNames = ['A', 'B', 'C']
                            if Value in GradeNames:
                                Value = 1 + GradeNames.index(Value)
                            else:
                                Value = int(Value)
                            if Value == 3:
                                DefectsDict[ModuleID]['GradeHR'] = 'C'
                            elif Value == 2:
                                DefectsDict[ModuleID]['GradeHR'] = 'B'
                        except:
                            self.ProblematicModulesList.append(ModuleID)
        ### ManualGradeHR
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ManualGrade', 'Value'])
                    if Value is not None:
                        try:
                            GradeNames = ['A', 'B', 'C']
                            if Value in GradeNames:
                                Value = 1 + GradeNames.index(Value)
                            else:
                                Value = int(Value)
                            if Value == 3:
                                DefectsDict[ModuleID]['ManualGradeHR'] = 'C'
                            elif Value == 2:
                                DefectsDict[ModuleID]['ManualGradeHR'] = 'B'
                            elif Value == 1:
                                # also list grade A here because it can negate effect of other defects!
                                DefectsDict[ModuleID]['ManualGradeHR'] = 'A'
                        except:
                            self.ProblematicModulesList.append(ModuleID)

        ### DEFECTS for defects.txt
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'XRayHRQualification', 'KeyValueDictPairs.json', 'SpecialDefects', 'Value'])
                    if Value is not None:
                        try:
                            DefectsList = [x.strip() for x in Value.split(',')]
                            for Defect in DefectsList:
                                if 'DEFECT_%s'%Defect not in DefectsDict[ModuleID]:
                                    DefectsDict[ModuleID]['DEFECT_%s'%Defect] = {}
                                DefectsDict[ModuleID]['DEFECT_%s'%Defect] = 'C'
                        except:
                            self.ProblematicModulesList.append(ModuleID)

        ### defectiveBumps X-ray
                    BBGrades = []
                    for Chip in range(0,16):
                        BBGradesROC = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'HitMapGrade', 'Value'])
                        if BBGradesROC:
                            for BBGradeROC in BBGradesROC.split("/"):
                                if not '(' in BBGradeROC and len(BBGradeROC)>0:
                                    BBGrades.append(BBGradeROC)
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                    if 'C' in BBGrades:
                        DefectsDict[ModuleID]['BB_X-ray'] = 'C'
                    elif 'B' in BBGrades:
                        DefectsDict[ModuleID]['BB_X-ray'] = 'B'

        ### lowEfficiency
                    EfficiencyGrades = []
                    for Chip in range(0,16):
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'EfficiencyGrade', 'Value'])
                        if Value is not None:
                            Grades = [grade for grade in Value.split('/') if grade and grade.strip()[0] != '(']
                            EfficiencyGrades += Grades
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                    if 'C' in EfficiencyGrades:
                        DefectsDict[ModuleID]['lowHREfficiency'] = 'C'
                    elif 'B' in EfficiencyGrades:
                        DefectsDict[ModuleID]['lowHREfficiency'] = 'B'

        ### double column ###
                    DoubleColumnGrades = []
                    for Chip in range(0,16):
                        Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'BadDoubleColumnsGrade', 'Value'])
                        if Value is not None:
                            Grades = [grade for grade in Value.split('/') if grade and grade.strip()[0] != '(']
                            DoubleColumnGrades += Grades
                        else:
                            self.ProblematicModulesList.append(ModuleID)
                    if 'C' in DoubleColumnGrades:
                        DefectsDict[ModuleID]['DoubleColumn'] = 'C'
                    elif 'B' in DoubleColumnGrades:
                        DefectsDict[ModuleID]['DoubleColumn'] = 'B'

        ### r/o problems
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ROCsWithReadoutProblems', 'Value'])
                    if Value is not None and Value > 0:
                        DefectsDict[ModuleID]['ReadoutProblems'] = 'C'
                    elif Value is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### unif problems
                    Value = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Grading', 'KeyValueDictPairs.json', 'ROCsWithUniformityProblems', 'Value'])
                    if Value is not None and Value > 0:
                        DefectsDict[ModuleID]['UniformityProblems'] = 'C'
                    elif Value is None:
                        self.ProblematicModulesList.append(ModuleID)

        ### X-ray noise
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
                        else:
                            self.ProblematicModulesList.append(ModuleID)

                    if 'C' in RocGrades:
                        DefectsDict[ModuleID]['Noise_X-ray'] = 'C'
                    elif 'B' in RocGrades:
                        DefectsDict[ModuleID]['Noise_X-ray'] = 'B'

        ### totalDefects X-ray
                    RocGrades = []
                    for Chip in range(0,16):
                        NDefects = self.GetJSONValue([ RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips', 'Chip%d'%Chip, 'Grading', 'KeyValueDictPairs.json', 'PixelDefects', 'Value'])
                        if NDefects:
                            NDefects = int(NDefects)
                            if NDefects >= GradePixelDefectsBC:
                                RocGrades.append('C')
                            elif  NDefects >= GradePixelDefectsAB:
                                RocGrades.append('B')
                        else:
                            self.ProblematicModulesList.append(ModuleID)

                    if 'C' in RocGrades:
                        DefectsDict[ModuleID]['TotalDefects_X-ray'] = 'C'
                    elif 'B' in RocGrades:
                        DefectsDict[ModuleID]['TotalDefects_X-ray'] = 'B'

        self.HiddenData['DefectsDict'] = DefectsDict
        # save defects dictionary as json file
        JsonFileName = ''
        try:
            JsonFileName = self.GlobalOverviewPath+'/'+self.Attributes['BasePath'] + '/KeyValueDictPairs.json'
            f = open(JsonFileName, 'w')
            f.write(json.dumps(DefectsDict, sort_keys=True, indent=4, separators=(',', ': '), cls=SetEncoder))
            f.close()
            print "    -> written to %s"%JsonFileName
        except:
            print "could not write json file: '%s'!"%JsonFileName

        # plot dictionary
        for ModuleID, Defects in DefectsDict.iteritems():
            #print "Module ",ModuleID
            BinNumber = 1 + ModuleIDsList.index(ModuleID)
            Summary.GetXaxis().SetBinLabel(BinNumber, ModuleID)
            for Defect, Grades in Defects.iteritems():
                #print " Defect: ", Defect
                if type(Grades) is dict:
                    for Test, Grade in Grades.iteritems():
                        #print "  Test:", Test, " -> Grade ", Grade
                        TestIndex = FullTests.index(Test)
                        if Defect in YLabels:
                            YPosition = 1 + 3*YLabels.index(Defect)
                            if Grade == 'C':
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ColorC)
                            elif Grade == 'B':
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ColorB)
                            elif Grade == 'A':
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ColorA)
                            else:
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ROOT.kBlue)
                else:
                    Grade = Grades.strip()
                    for TestIndex in range(0,3):
                        if Defect in YLabels:
                            YPosition = 1 + 3*YLabels.index(Defect)
                            if Grade == 'C':
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ColorC)
                            elif Grade == 'B':
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ColorB)
                            elif Grade == 'A':
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ColorA)
                            else:
                                Summary.SetBinContent(BinNumber, YPosition + TestIndex, ROOT.kBlue)
 

        ROOT.gPad.SetLeftMargin(0.16)
        ROOT.gPad.SetRightMargin(0.03)
        Summary.Draw("col")
        Summary.GetZaxis().SetRangeUser(0, 1.0)
        Summary.GetYaxis().SetLabelSize(0.045)

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
        line1.SetLineWidth(1)
        try:
            line1.SetLineColorAlpha(ROOT.kBlack, 0.35)
        except:
            line1.SetLineColor(ROOT.kBlack) # for old root versions

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

