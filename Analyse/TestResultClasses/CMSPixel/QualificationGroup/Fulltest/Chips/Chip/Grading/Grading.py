import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

try:
       set
except NameError:
       from sets import Set as set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.ResultData['HiddenData']['DeadPixelList'] = set()
        self.ResultData['HiddenData']['Noisy1PixelList'] = set()
        self.ResultData['HiddenData']['MaskDefectList'] = set()
        self.ResultData['HiddenData']['IneffPixelList'] = set()

        self.ResultData['HiddenData']['AddressProblemList'] = set()
        self.ResultData['HiddenData']['ThrDefectList'] = set()
        self.ResultData['HiddenData']['NoisyPixelSCurveList'] = set()
        self.ResultData['HiddenData']['GainDefectList'] = set()
        self.ResultData['HiddenData']['PedDefectList'] = set()
        self.ResultData['HiddenData']['Par1DefectList'] = set()
        self.ResultData['HiddenData']['TotalList'] = set()
        self.isDigitalROC = self.ParentObject.ParentObject.ParentObject.Attributes['isDigital']

    def GetSingleChipSubtestGrade(self, SpecialPopulateDataParameters, CurrentGrade):
	Value = float(self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs'][SpecialPopulateDataParameters['DataParameterKey']]['Value'])
	nValue = float(self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs']['N']['Value'])
	
	if SpecialPopulateDataParameters.has_key('DataFactor'):
		Value = Value*SpecialPopulateDataParameters['DataFactor']
	if SpecialPopulateDataParameters.has_key('CalcFunction'):
		Value = SpecialPopulateDataParameters['CalcFunction'](Value, self.ParentObject.ResultData['SubTestResults'][SpecialPopulateDataParameters['DataKey']].ResultData['KeyValueDictPairs'])
	
	Value = float(Value)
	ChipGrade = CurrentGrade
	
	if ChipGrade == 1 and Value > SpecialPopulateDataParameters['YLimitB']:
		ChipGrade = 2
	if Value > SpecialPopulateDataParameters['YLimitC']:
		ChipGrade = 3
	if ChipGrade == 1 and nValue < (8*self.nCols - self.TestResultEnvironmentObject.GradingParameters['defectsB']):
		ChipGrade = 2
	if nValue < (8*self.nCols - self.TestResultEnvironmentObject.GradingParameters['defectsC']):
		ChipGrade = 3
	return ChipGrade
	
#     def HasBumpBondingProblems(self,column,row,threshold):
#         binContent = self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject'].GetBinContent(column+1, row+1)
#         if self.isDigitalROC:
#             if binContent >= threshold:
#                 self.ResultData['HiddenData']['DeadBumpList'].add((self.chipNo,column,row))
#                 return True
#         else:# is analog ROC
#             if binContent >= self.TestResultEnvironmentObject.GradingParameters['minThrDiff']:#analog Roc
#                 self.ResultData['HiddenData']['DeadBumpList'].add((self.chipNo,column,row))
#                 return True
#         return False

    # todo: think about counting of dead trim bits
#     def HasDeadTrimBit(self,column,row,TrimBitHistograms):
#         gradingCriteria = self.TestResultEnvironmentObject.GradingParameters['TrimBitDifference']
#         for k in range(1,5):
#             trimBit0 = TrimBitHistograms[0].GetBinContent(column+1, row+1)
#             trimBitK = TrimBitHistograms[k].GetBinContent(column+1, row+1)
#             TrimBitDifference = abs( trimBitK- trimBit0)
#             if TrimBitDifference  <= gradingCriteria :
# #                 print 'added', column,row,trimBitK,trimBit0,TrimBitDifference,gradingCriteria,(gradingCriteria  <=  gradingCriteria)
#                 self.ResultData['HiddenData']['DeadTrimbitsList'].add((self.chipNo,column,row))
#                 return True
#         return False

#     def HasAddressDecodingProblem(self,column,row):
#         if self.ParentObject.ResultData['SubTestResults']['AddressDecoding'].ResultData['Plot']['ROOTObject'].GetBinContent(column+1, row+1) < 1:
#             self.ResultData['HiddenData']['AddressProblemList'].add((self.chipNo,column,row))
#             return True
#         return False

#     def HasThresholdDefect(self,column,row,VcalThresholdMapHistogram):
#         if self.ParentObject.ResultData['SubTestResults']['OpParameters'].ResultData['HiddenData'].has_key('vcalTrim'):
#             binContent = VcalThresholdMapHistogram.GetBinContent(column+1,row+1)
#             vcalTrim = self.ParentObject.ResultData['SubTestResults']['OpParameters'].ResultData['HiddenData']['vcalTrim']
#             if abs(binContent - vcalTrim) > self.TestResultEnvironmentObject.GradingParameters['tthrTol']:
#                 self.ResultData['HiddenData']['ThrDefectList'].add((self.chipNo,column,row))
#                 return True
#         return False

    def IsNoisyPixelSCurve(self,column,row):
        LineArray = self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].FileHandle.readline().strip().split()
        try:
            if (float(LineArray[1]) < self.TestResultEnvironmentObject.GradingParameters['noiseMin']) or (float(LineArray[1]) > self.TestResultEnvironmentObject.GradingParameters['noiseMax']):
                self.ResultData['HiddenData']['NoisyPixelSCurveList'].add((self.chipNo,column,row))
        except (ValueError, TypeError, IndexError):
            pass
    def HasPar1Problem(self,column,row):
        LineArray = self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].FileHandle.readline().strip().split()
        try:
            fl1 = float(LineArray[1])
            if  (fl1 < self.TestResultEnvironmentObject.GradingParameters['par1Min']) or (fl1 > self.TestResultEnvironmentObject.GradingParameters['par1Max']) :
#
#                 if px_counted:
#                     nDoubleCounts+=1
#                 px_counted = 1
#
#                 if px_perf_counted:
#                     nDoublePerfCounts+=1
#                 px_perf_counted = 1
#
#                 if ph_counted:
#                     nDoublePHs+=1
#                 ph_counted = 1
#
#                 nPar1Defect+=1
                self.ResultData['HiddenData']['Par1DefectList'].add((self.chipNo,column,row))
        except (ValueError, TypeError, IndexError):
            pass

    #todo
#     def HasBadGainValue(self,column,row):
#         LineArray = self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.readline().strip().split()
#         try:
#             fl2 = float(LineArray[2])
#             if fl2 != 0:
#                 gain = 1./fl2
#             ped = fl3
#             if  (gain < self.TestResultEnvironmentObject.GradingParameters['gainMin']) or (gain > self.TestResultEnvironmentObject.GradingParameters['gainMax']) :
#                 #todo
#                 self.ResultData['HiddenData']['GainDefectList'].add((self.chipNo,column,row))
#         except (ValueError, TypeError, IndexError):
#             pass
#     #todo
#     def HasBadPedestalValue(self,column,row):
#         if (ped < self.ParentObject.ResultData['SubTestResuts'].PHCalibrationPedestal.ResultData['HiddenData']['PedestalMin']) or (ped > self.ParentObject.ResultData['SubTestResuts'].PHCalibrationPedestal.ResultData['HiddenData']['PedestalMax']) :
#             self.ResultData['HiddenData']['PedDefectList'].add((self.chipNo,column,row))
#             return True
#         return False


    def PopulateResultData(self):
#         nMaskDefect = 0
#         nDeadBumps = 0
#         nDeadTrimbits = 0
#
#         nAddressProblems = 0
#
#         nNoisy2Pixel = 0
#         nThrDefect = 0
#         nGainDefect = 0
#         nPar1Defect = 0
#         nRootFileProblems = 0
#
#         nDoubleFunctCounts = 0
#         nDoublePerfCounts = 0
#         nDoubleCounts = 0
#         nDoubleTrims = 0
#         nDoublePHs = 0

        BumpBondingProblems_Mean = self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Mean']['Value']
        BumpBondingProblems_RMS = self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['RMS']['Value']
        BumpBondingProblems_nSigma = 0
        if self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs'].has_key('nSigma'):
            BumpBondingProblems_nSigma = self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['nSigma']['Value']

#         print 'Chip No.: %s'%self.chipNo
#         print 'isDigitalROC: %s'%self.isDigitalROC
#         print ' BumpBondingProblems_Mean: %s'%BumpBondingProblems_Mean
#         print ' BumpBondingProblems_RMS: %s'%BumpBondingProblems_RMS
#         print ' BumpBondingProblems_nSigma: %s'%BumpBondingProblems_nSigma
#         if self.isDigitalROC:

        TrimBitHistograms = []
        ChipNo=self.ParentObject.Attributes['ChipNo']
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        for k in range(5):
            histname = HistoDict.get('Summary','TrimBitMap%d'%k)
            tmpHistogram = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            tmpHistogram = tmpHistogram.Clone(self.GetUniqueID())
            TrimBitHistograms.append(tmpHistogram )

        # TH2D

        histname = HistoDict.get('Summary','ThresholdMap')
        tmpHistogram = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
        VcalThresholdMapHistogram =  tmpHistogram.Clone(self.GetUniqueID())

        #reset file pointers
        # if self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].FileHandle:
            # self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].FileHandle.seek(0)
            # for i in range(2):
                # self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.readline() #Omit first three lines
# 
        # if self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle:
            # self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.seek(0)
            # for i in range(4):
                # self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.readline() #Omit first three lines
# 
        # if self.ParentObject.Attributes['ModuleVersion'] == 1:
            # if self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan']:
                # self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].FileHandle.seek(0)
                # for i in range(3):
                    # self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].FileHandle.readline() #Omit first three lines

        notAlivePixels = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NotAlivePixels']['Value']
        for column in range(self.nCols): #Column
            for row in range(self.nRows): #Row
                # -- Bump bonding
                if  (self.chipNo,column,row) not in notAlivePixels:
                    pass
#                     self.HasBumpBondingProblems(column,row,BumpBondingProblems_Mean+ BumpBondingProblems_nSigma * BumpBondingProblems_RMS)
#                     self.HasDeadTrimBit(column, row, TrimBitHistograms)
#                     self.HasAddressDecodingProblem(column,row)
#                     self.HasThresholdDefect(column,row,VcalThresholdMapHistogram)
                    #self.IsNoisyPixelSCurve(column,row)
#                     self.HasBadPedestalValue(column,row)
#                     self.HasBadGainValue(column,row)
#                     self.HasPar1Problem(column,row)
        self.ResultData['HiddenData']['ThrDefectList'] = self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['TrimProblems']['Value']
        self.ResultData['HiddenData']['AddressProblemList'] = self.ParentObject.ResultData['SubTestResults']['AddressDecoding'].ResultData['KeyValueDictPairs']['AddressDecodingProblems']['Value']
        self.ResultData['HiddenData']['DeadBumpList'] = self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['DeadBumps']['Value']
        self.ResultData['HiddenData']['DeadTrimbitsList'] = self.ParentObject.ResultData['SubTestResults']['TrimBitProblems'].ResultData['KeyValueDictPairs']['DeadTrimbits']['Value']
        self.ResultData['HiddenData']['DeadPixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        self.ResultData['HiddenData']['Noisy1PixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value']
        self.ResultData['HiddenData']['MaskDefectList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['MaskDefects']['Value']
        self.ResultData['HiddenData']['IneffPixelList'] = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['InefficentPixels']['Value']
        self.ResultData['HiddenData']['DeadTrimbitsList'] = self.ResultData['HiddenData']['DeadTrimbitsList'] - self.ResultData['HiddenData']['DeadPixelList']
        self.ResultData['HiddenData']['MaskDefectList'] = self.ResultData['HiddenData']['MaskDefectList'] - self.ResultData['HiddenData']['DeadPixelList']
        self.ResultData['HiddenData']['AddressProblemList'] = self.ResultData['HiddenData']['AddressProblemList'] - self.ResultData['HiddenData']['DeadPixelList']
        self.ResultData['HiddenData']['DeadBumpList'] = self.ResultData['HiddenData']['DeadBumpList'] - self.ResultData['HiddenData']['DeadPixelList']
        self.ResultData['HiddenData']['TotalList'] = self.ResultData['HiddenData']['DeadPixelList'].union(self.ResultData['HiddenData']['MaskDefectList']).union(self.ResultData['HiddenData']['DeadTrimbitsList']).union(self.ResultData['HiddenData']['AddressProblemList']).union(self.ResultData['HiddenData']['DeadBumpList'])

        if True or (len(self.ResultData['HiddenData']['TotalList']) > 0) :
            print '\nChip %d'%self.chipNo

#             print self.ResultData['HiddenData']['TotalList']
            print '\ttotal: %4d'%len(self.ResultData['HiddenData']['TotalList'])
            print '\tdead:  %4d'%len(self.ResultData['HiddenData']['DeadPixelList'])
            print '\tmask:  %4d'%len(self.ResultData['HiddenData']['MaskDefectList'])
            print '\ttrim:  %4d'%len(self.ResultData['HiddenData']['DeadTrimbitsList'])
            print '\taddr:  %4d'%len(self.ResultData['HiddenData']['AddressProblemList'])
            print '\tbump:  %4d' % len(self.ResultData['HiddenData']['DeadBumpList'])

#                 = %d + %d + %d + %d'%(len(self.ResultData['HiddenData']['TotalList']),len(self.ResultData['HiddenData']['DeadPixelList']) , len(self.ResultData['HiddenData']['MaskDefectList']) , len(self.ResultData['HiddenData']['DeadTrimbitsList']) , len(self.ResultData['HiddenData']['AddressProblemList']))
        # -- Compute the final verdict on this chip  //?? FIXME (below is pure randomness)
        # finalVerdict = 0
        # if len(self.ResultData['HiddenData']['DeadTrimbitsList']) > 0:
            # finalVerdict += 1
        # if len(self.ResultData['HiddenData']['DeadPixelList']) > 0:
            # finalVerdict += 10
        # if len(self.ResultData['HiddenData']['Noisy1PixelList']) > 0:
            # finalVerdict += 10
        # if len(self.ResultData['HiddenData']['AddressProblemList']) > 0:
            # finalVerdict += 10
        # if len(self.ResultData['HiddenData']['DeadBumpList']) > 0:
            # finalVerdict += 100
        # if len(self.ResultData['HiddenData']['NoisyPixelSCurveList']) > 0:
            # finalVerdict += 1000
        # if len(self.ResultData['HiddenData']['ThrDefectList']) > 0:
# #             print 'ThrDefects: %s'%nThrDefect
# #             print len(ThrDefectList), ThrDefectList
            # finalVerdict += 10000
        # if len(self.ResultData['HiddenData']['GainDefectList']) > 0:
            # finalVerdict += 100000
        # if len(self.ResultData['HiddenData']['PedDefectList']) > 0:
            # finalVerdict += 100000
        # if len(self.ResultData['HiddenData']['Par1DefectList']) > 0:
            # finalVerdict += 100000
            # 
            # 
            
            
            
        PixelDefectsGradeALimit = self.TestResultEnvironmentObject.GradingParameters['defectsB']
        PixelDefectsGradeBLimit = self.TestResultEnvironmentObject.GradingParameters['defectsC']
        totalDefects = len(self.ResultData['HiddenData']['TotalList'])
        if totalDefects < PixelDefectsGradeALimit:
            pixelDefectsGrade = 1
        elif totalDefects < PixelDefectsGradeBLimit:
            pixelDefectsGrade = 2
        else:
            pixelDefectsGrade = 3
        print '\tGrade: %s'%pixelDefectsGrade
        self.ResultData['KeyValueDictPairs'] = {
            'PixelDefectsGrade':{
                'Value': '%d'%pixelDefectsGrade,
                'Label': 'Pixel Defects Grade ROC'
            },
        }
        self.ResultData['KeyList'] = ['PixelDefectsGrade']

