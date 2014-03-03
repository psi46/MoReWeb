import ROOT
import AbstractClasses
from sets import Set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_Summary_TestResult'
        self.NameSingle='Summary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        self.DeadPixelList = Set()
        self.Noisy1PixelList = Set()
        self.MaskDefectList = Set()
        self.IneffPixelList = Set()
        self.DeadBumpList = Set()
        self.DeadTrimbitsList = Set()
        self.AddressProblemList = Set()
        self.ThrDefectList = Set()
        self.NoisyPixelSCurveList = Set()
        self.GainDefectList = Set()
        self.PedDefectList = Set()
        self.Par1DefectList = Set()
        self.isDigitalROC = self.ParentObject.ParentObject.ParentObject.Attributes['isDigital']
        


    
    def HasBumpBondingProblems(self,column,row,threshold):
        binContent = self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject'].GetBinContent(column+1, row+1)
        if self.isDigitalROC:
            if binContent >= threshold:
                self.DeadBumpList.add((self.chipNo,column,row))
                return True
        else:# is analog ROC    
            if binContent >= self.TestResultEnvironmentObject.GradingParameters['minThrDiff']:#analog Roc
                self.DeadBumpList.add((self.chipNo,column,row))
                return True
        return False
    
    # todo: think about counting of dead trim bits 
    def HasDeadTrimBit(self,column,row,TrimBitHistograms):
        gradingCriteria = self.TestResultEnvironmentObject.GradingParameters['TrimBitDifference']
        for k in range(1,5):
            trimBit0 = TrimBitHistograms[0].GetBinContent(column+1, row+1)
            trimBitK = TrimBitHistograms[k].GetBinContent(column+1, row+1)
            TrimBitDifference = abs( trimBitK- trimBit0)
            if TrimBitDifference  <= gradingCriteria :
#                 print 'added', column,row,trimBitK,trimBit0,TrimBitDifference,gradingCriteria,(gradingCriteria  <=  gradingCriteria)
                self.DeadTrimbitsList.add((self.chipNo,column,row))
                return True
        return False
    
    def HasAddressDecodingProblem(self,column,row):
        if self.ParentObject.ResultData['SubTestResults']['AddressDecoding'].ResultData['Plot']['ROOTObject'].GetBinContent(column+1, row+1) < 1:
            self.AddressProblemList.add((self.chipNo,column,row))
            return True
        return False
                
    def HasThresholdDefect(self,column,row,VcalThresholdMapHistogram):
        if self.ParentObject.ResultData['SubTestResults']['OpParameters'].ResultData['HiddenData'].has_key('vcalTrim'):
            binContent = VcalThresholdMapHistogram.GetBinContent(column+1,row+1)
            vcalTrim = self.ParentObject.ResultData['SubTestResults']['OpParameters'].ResultData['HiddenData']['vcalTrim']
            if abs(binContent - vcalTrim) > self.TestResultEnvironmentObject.GradingParameters['tthrTol']:
                self.ThrDefectList.add((self.chipNo,column,row))
                return True
        return False
    
    def IsNoisyPixelSCurve(self,column,row):
        LineArray = self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].FileHandle.readline().strip().split()
        try:
            if (float(LineArray[1]) < self.TestResultEnvironmentObject.GradingParameters['noiseMin']) or (float(LineArray[1]) > self.TestResultEnvironmentObject.GradingParameters['noiseMax']):
                self.NoisyPixelSCurveList.add((self.chipNo,column,row))
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
                self.Par1DefectList.add((self.chipNo,column,row))
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
#                 self.GainDefectList.add((self.chipNo,column,row))
#         except (ValueError, TypeError, IndexError):
#             pass
#     #todo
#     def HasBadPedestalValue(self,column,row):
#         if (ped < self.ParentObject.ResultData['SubTestResuts'].PHCalibrationPedestal.ResultData['HiddenData']['PedestalMin']) or (ped > self.ParentObject.ResultData['SubTestResuts'].PHCalibrationPedestal.ResultData['HiddenData']['PedestalMax']) :
#             self.PedDefectList.add((self.chipNo,column,row))
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
        fileHandle = self.ParentObject.ParentObject.FileHandle
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        for k in range(5):
            histname = HistoDict.get(self.NameSingle,'TrimBitMap%d'%k)%ChipNo
            tmpHistogram = fileHandle.Get(histname).Clone(self.GetUniqueID())
            TrimBitHistograms.append(tmpHistogram )
        
        # TH2D
        
        histname = HistoDict.get(self.NameSingle,'ThresholdMap')%ChipNo
        VcalThresholdMapHistogram =  fileHandle.Get(histname).Clone(self.GetUniqueID())
        
        #reset file pointers
        if self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].FileHandle:
            self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].FileHandle.seek(0)
            for i in range(2):
                self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.readline() #Omit first three lines
        
        if self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle:
            self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.seek(0)
            for i in range(4):
                self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.readline() #Omit first three lines
        
        if self.ParentObject.Attributes['ModuleVersion'] == 1:
            if self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan']:
                self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].FileHandle.seek(0)
                for i in range(3):
                    self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].FileHandle.readline() #Omit first three lines
        
        notAlivePixels = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NotAlivePixels']['Value']
        for column in range(self.nCols): #Column
            for row in range(self.nRows): #Row
                # -- Bump bonding
                if  (self.chipNo,column,row) not in notAlivePixels:
                    self.HasBumpBondingProblems(column,row,BumpBondingProblems_Mean+ BumpBondingProblems_nSigma * BumpBondingProblems_RMS)
                    self.HasDeadTrimBit(column, row, TrimBitHistograms)
                    self.HasAddressDecodingProblem(column,row)
                    self.HasThresholdDefect(column,row,VcalThresholdMapHistogram)
                    #self.IsNoisyPixelSCurve(column,row)
#                     self.HasBadPedestalValue(column,row)
#                     self.HasBadGainValue(column,row)
#                     self.HasPar1Problem(column,row)
        self.DeadPixelList = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        self.Noisy1PixelList = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value']
        self.MaskDefectList = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['MaskDefects']['Value']
        self.IneffPixelList = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['InefficentPixels']['Value']
        totalList = self.DeadPixelList.union(self.MaskDefectList).union(self.DeadTrimbitsList).union(self.AddressProblemList)
        
        if True or (len(totalList) > 0) :
            print '\nChip %d'%self.chipNo
            
#             print totalList
            print '\ttotal: %4d'%len(totalList)
            print '\tdead:  %4d'%len(self.DeadPixelList)
            print '\tmask:  %4d'%len(self.MaskDefectList)
            print '\ttrim:  %4d'%len(self.DeadTrimbitsList)
            print '\taddr:  %4d'%len(self.AddressProblemList)
#                 = %d + %d + %d + %d'%(len(totalList),len(self.DeadPixelList) , len(self.MaskDefectList) , len(self.DeadTrimbitsList) , len(self.AddressProblemList))
        # -- Compute the final verdict on this chip  //?? FIXME (below is pure randomness)
        finalVerdict = 0
        if len(self.DeadTrimbitsList) > 0:
            finalVerdict += 1
        if len(self.DeadPixelList) > 0:
            finalVerdict += 10
        if len(self.Noisy1PixelList) > 0:
            finalVerdict += 10
        if len(self.AddressProblemList) > 0:
            finalVerdict += 10
        if len(self.DeadBumpList) > 0:
            finalVerdict += 100
        if len(self.NoisyPixelSCurveList) > 0:
            finalVerdict += 1000
        if len(self.ThrDefectList) > 0:
#             print 'ThrDefects: %s'%nThrDefect
#             print len(ThrDefectList), ThrDefectList
            finalVerdict += 10000
        if len(self.GainDefectList) > 0:
            finalVerdict += 100000
        if len(self.PedDefectList) > 0:
            finalVerdict += 100000
        if len(self.Par1DefectList) > 0:
            finalVerdict += 100000
        gradeA = self.TestResultEnvironmentObject.GradingParameters['defectsB']
        gradeB = self.TestResultEnvironmentObject.GradingParameters['defectsC']
        totalDefects = len(totalList)
        if totalDefects < gradeA:
            pixelDefectsGrade = 1
        elif totalDefects < gradeB:
            pixelDefectsGrade = 2
        else:
            pixelDefectsGrade = 3
        print '\tGrade: %s'%pixelDefectsGrade
        self.ResultData['KeyValueDictPairs'] = {
            'Total': {
                'Value':'{0:1.0f}'.format(len(totalList)), 
                'Label':'Total'
            },
            'nDeadPixel': {
                'Value':'{0:1.0f}'.format(len(self.DeadPixelList)), 
                'Label':'Dead Pixels'
            },
            'nNoisy1Pixel': {
                'Value':'{0:1.0f}'.format(len(self.Noisy1PixelList)), 
                'Label':'Noisy Pixels 1'
            },
            'nMaskDefect': {
                'Value':'{0:1.0f}'.format(len(self.MaskDefectList)), 
                'Label':'Mask Defects'
            },
            'nDeadBumps': {
                'Value':'{0:1.0f}'.format(len(self.DeadBumpList)), 
                'Label':'Dead Bumps'
            },
            'nDeadTrimbits': {
                'Value':'{0:1.0f}'.format(len(self.DeadTrimbitsList)), 
                'Label':'Dead Trimbits'
            },
            'nAddressProblems': {
                'Value':'{0:1.0f}'.format(len(self.AddressProblemList)), 
                'Label':'Address Problems'
            },
            'nNoisy2Pixel': {
                'Value':'{0:1.0f}'.format(len(self.NoisyPixelSCurveList)), 
                'Label':'Noisy Pixels 2'
            },
            'nThrDefect': {
                'Value':'{0:1.0f}'.format(len(self.NoisyPixelSCurveList)), 
                'Label':'Trim Problems'
            },
            'nGainDefect': {
                'Value':'{0:1.0f}'.format(len(self.GainDefectList)), 
                'Label':'PH Gain defects'
            },
            'nPedDefect': {
                'Value':'{0:1.0f}'.format(len(self.PedDefectList)), 
                'Label':'PH Pedestal defects'
            },
            'nPar1Defect': {
                'Value':'{0:1.0f}'.format(len(self.Par1DefectList)), 
                'Label':'PH Parameter1 Defects'
            },
            'PixelDefectsGrade':{
                'Value': '%d'%pixelDefectsGrade,
                'Label': 'Pixel Defects Grade ROC'
            }
        }
        self.ResultData['KeyList'] = ['Total','nDeadPixel','nNoisy1Pixel','nMaskDefect','nDeadBumps','nDeadTrimbits'
                                      ,'nAddressProblems','nNoisy2Pixel','nThrDefect','nGainDefect','nPedDefect','nPar1Defect','PixelDefectsGrade']
    
