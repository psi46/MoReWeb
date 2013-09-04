import ROOT
import AbstractClasses
from sets import Set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_Summary_TestResult'
        self.NameSingle='Summary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.chipNo = self.ParentObject.Attributes['ChipNo']
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        nDeadPixel = 0
        DeadPixelList = Set()
        nIneffPixel = 0
        IneffPixelList = Set()
        nMaskDefect = 0
        MaskDefectList = Set()
        nNoisy1Pixel = 0
        Noisy1PixelList = Set()
        nDeadBumps = 0
        DeadBumpList = Set()
        nDeadTrimbits = 0
        DeadTrimbitsList = Set()
        nAddressProblems = 0
        AddressProblemList = Set()
    
        nNoisy2Pixel = 0
        Noisy2PixelList = Set()
        nThrDefect = 0
        ThrDefectList = Set()
        nGainDefect = 0
        GainDefectList = Set()
        nPedDefect = 0
        PedDefectList = Set()
        nPar1Defect = 0
        Par1DefectList = Set()
    
        nRootFileProblems = 0
    
        nDoubleFunctCounts = 0
        nDoublePerfCounts = 0
        nDoubleCounts = 0
        nDoubleTrims = 0
        nDoublePHs = 0
        
        
        TrimBitHistograms = []
        for k in range(5):
            tmpHistogram = self.ParentObject.ParentObject.FileHandle.Get("CalThresholdMap_C{ChipNo};{pos}".format(ChipNo=self.ParentObject.Attributes['ChipNo'], pos=k+1) ).Clone(self.GetUniqueID())
            TrimBitHistograms.append(tmpHistogram )
            
        
        # TH2D
        VcalThresholdMapHistogram =  self.ParentObject.ParentObject.FileHandle.Get("VcalThresholdMap_C{ChipNo};8".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())
        
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
            
        for column in range(52): #Column
            for row in range(80): #Row
            	i = column
            	j = row
                
                pixel_alive   = 1
                px_funct_counted = 0
                px_perf_counted = 0
                px_counted = 0
        
                trim_counted = 0
                ph_counted = 0
        
                PixelMapCurrentValue = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['Plot']['ROOTObject'].GetBinContent(i+1, j+1)
                
                # -- Pixel alive
                if PixelMapCurrentValue == 0:
                    
                    pixel_alive = 0
                    nDeadPixel += 1
                    DeadPixelList.add((self.chipNo,column,row))
                    
                elif PixelMapCurrentValue  > self.TestResultEnvironmentObject.GradingParameters['PixelMapMaxValue']:
                    nNoisy1Pixel += 1
                    Noisy1PixelList.add((self.chipNo,column,row))
                    px_counted = 1 
                    px_funct_counted = 1
                elif PixelMapCurrentValue  < self.TestResultEnvironmentObject.GradingParameters['PixelMapMinValue']:
                    nMaskDefect += 1
                    MaskDefectList.add((self.chipNo,column,row))  
                    px_counted = 1
                    px_funct_counted = 1
                else:
                    nIneffPixel += 1
                    IneffPixelList.add((self.chipNo,column,row))
                    px_counted = 1
                    px_funct_counted = 1
        
        
                # -- Bump bonding
                if  pixel_alive and self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject'].GetBinContent(i+1, j+1) >= self.TestResultEnvironmentObject.GradingParameters['minThrDiff']:
                    
                        if px_counted:
                            nDoubleCounts += 1
                            
                        px_counted = 1
                
                        if px_funct_counted:
                            nDoubleFunctCounts += 1
                            
                        px_funct_counted = 1
                
                        nDeadBumps += 1
                        DeadBumpList.add((self.chipNo,column,row))

        
                # -- Trim bits 1 - 4
                if pixel_alive:
                    for k in range(1,5):
                        TrimBitDifference = ROOT.TMath.Abs(TrimBitHistograms[k].GetBinContent(i+1, j+1) - TrimBitHistograms[0].GetBinContent(i+1, j+1))
                        
                        if TrimBitDifference  <= self.TestResultEnvironmentObject.GradingParameters['TrimBitDifference'] :
                            if px_counted:
                                nDoubleCounts+=1
                            px_counted = 1
                
                            if px_funct_counted:
                                nDoubleFunctCounts+=1
                            px_funct_counted = 1
                
                            if trim_counted:
                                nDoubleTrims+=1
                            trim_counted = 1
                
                            nDeadTrimbits+=1
                            DeadTrimbitsList.add((self.chipNo,column,row))

                # -- Address decoding
                if pixel_alive:
                    if self.ParentObject.ResultData['SubTestResults']['AddressDecoding'].ResultData['Plot']['ROOTObject'].GetBinContent(i+1, j+1) < 1:
            
                        if px_counted:
                            nDoubleCounts+=1
                        px_counted = 1
                
                        if px_funct_counted:
                            nDoubleFunctCounts+=1
                        px_funct_counted = 1
                
                        nAddressProblems+=1
                        AddressProblemList.add((self.chipNo,column,row))
                
        
                # -- Threshold
                if pixel_alive:
                    if self.ParentObject.ResultData['SubTestResults']['OpParameters'].ResultData['HiddenData'].has_key('vcalTrim'):
                        if ROOT.TMath.Abs(VcalThresholdMapHistogram.GetBinContent(i+1, j+1) - self.ParentObject.ResultData['SubTestResults']['OpParameters'].ResultData['HiddenData']['vcalTrim']) > self.TestResultEnvironmentObject.GradingParameters['tthrTol']:
                            if px_counted:
                                nDoubleCounts+=1
                            px_counted = 1
                    
                            if px_perf_counted:
                                nDoublePerfCounts+=1
                            px_perf_counted = 1
                    
                            nThrDefect+=1
                            ThrDefectList.add((self.chipNo,column,row))
                                
        
                # -- Noise
                if pixel_alive and False:
                    LineArray = self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].FileHandle.readline().strip().split()
                    try:
                        
                        if (float(LineArray[1]) < self.TestResultEnvironmentObject.GradingParameters['noiseMin']) or (float(LineArray[1]) > self.TestResultEnvironmentObject.GradingParameters['noiseMax']):
                            if px_counted:
                                nDoubleCounts+=1
                            px_counted = 1
                    
                            if px_perf_counted:
                                nDoublePerfCounts+=1
                            px_perf_counted = 1
                    
                            nNoisy2Pixel+=1
                            Noisy2PixelList.add((self.chipNo,column,row))
                    except (ValueError, TypeError, IndexError):
                        pass
        
                # -- Gain & Pedestal
                if pixel_alive and False:
                    LineArray = self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].FileHandle.readline().strip().split()
                    try:
                        fl2 = float(LineArray[2])
                        if fl2 != 0:
                            gain = 1./fl2
                        ped = fl3
                
                        if  (gain < self.TestResultEnvironmentObject.GradingParameters['gainMin']) or (gain > self.TestResultEnvironmentObject.GradingParameters['gainMax']) :
                
                            if px_counted:
                                nDoubleCounts+=1
                            px_counted = 1
                    
                            if px_perf_counted:
                                nDoublePerfCounts+=1
                            px_perf_counted = 1
                    
                            if ph_counted:
                                nDoublePHs+=1
                            ph_counted = 1
                    
                            nGainDefect+=1
                    except (ValueError, TypeError, IndexError):
                        pass
            
                    if (ped < self.ParentObject.ResultData['SubTestResuts'].PHCalibrationPedestal.ResultData['HiddenData']['PedestalMin']) or (ped > self.ParentObject.ResultData['SubTestResuts'].PHCalibrationPedestal.ResultData['HiddenData']['PedestalMax']) :
            
                        if px_counted:
                            nDoubleCounts+=1
                        px_counted = 1
                
                        if px_perf_counted:
                            nDoublePerfCounts+=1
                        px_perf_counted = 1
                
                        if ph_counted:
                            nDoublePHs+=1
                        ph_counted = 1
                
                        nPedDefect+=1
                        PedDefectList.add((self.chipNo,column,row))
        
        
                # -- Par1
                if pixel_alive and False:
                    LineArray = self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].FileHandle.readline().strip().split()
                    try:
                        fl1 = float(LineArray[1])
                        if  (fl1 < self.TestResultEnvironmentObject.GradingParameters['par1Min']) or (fl1 > self.TestResultEnvironmentObject.GradingParameters['par1Max']) :
                
                            if px_counted:
                                nDoubleCounts+=1
                            px_counted = 1
                    
                            if px_perf_counted:
                                nDoublePerfCounts+=1
                            px_perf_counted = 1
                    
                            if ph_counted:
                                nDoublePHs+=1
                            ph_counted = 1
                    
                            nPar1Defect+=1
                            Par1DefectList.add((self.chipNo,column,row))
                    except (ValueError, TypeError, IndexError):
                        pass    
        
        Total = nDeadPixel + nMaskDefect + nDeadTrimbits + nAddressProblems
        totalList = DeadPixelList.union(MaskDefectList).union(DeadTrimbitsList).union(AddressProblemList)
        
        if False and (len(totalList) >0 or Total >0) :
            print '\nChip %d'%self.chipNo
            print '%d = %d + %d + %d + %d'%(Total,nDeadPixel , nMaskDefect , nDeadTrimbits , nAddressProblems)
            
            print totalList
            print '%d = %d + %d + %d + %d'%(len(totalList),len(DeadPixelList) , len(MaskDefectList) , len(DeadTrimbitsList) , len(AddressProblemList))
            if len(totalList) != Total:
                raw_input('Please check List, something is wrong')
#         raw_input('check both')
        # -- Compute the final verdict on this chip  //?? FIXME (below is pure randomness)
        finalVerdict = 0
        if nDeadTrimbits > 0:
            finalVerdict += 1
        if nDeadPixel > 0:
            finalVerdict += 10
        if nNoisy1Pixel > 0:
            finalVerdict += 10
        if nAddressProblems > 0:
            finalVerdict += 10
        if nDeadBumps > 0:
            finalVerdict += 100
        if nNoisy2Pixel > 0:
            finalVerdict += 1000
        if nThrDefect > 0:
#             print 'ThrDefects: %s'%nThrDefect
#             print len(ThrDefectList), ThrDefectList
            finalVerdict += 10000
        if nGainDefect > 0:
            finalVerdict += 100000
        if nPedDefect > 0:
            finalVerdict += 100000
        if nPar1Defect > 0:
            finalVerdict += 100000
            
        self.ResultData['KeyValueDictPairs'] = {
            'Total': {
                'Value':'{0:1.0f}'.format(Total), 
                'Label':'Total'
            },
            'nDeadPixel': {
                'Value':'{0:1.0f}'.format(nDeadPixel), 
                'Label':'Dead Pixels'
            },
            'nNoisy1Pixel': {
                'Value':'{0:1.0f}'.format(nNoisy1Pixel), 
                'Label':'Noisy Pixels 1'
            },
            'nMaskDefect': {
                'Value':'{0:1.0f}'.format(nMaskDefect), 
                'Label':'Mask Defects'
            },
            'nDeadBumps': {
                'Value':'{0:1.0f}'.format(nDeadBumps), 
                'Label':'Dead Bumps'
            },
            'nDeadTrimbits': {
                'Value':'{0:1.0f}'.format(nDeadTrimbits), 
                'Label':'Dead Trimbits'
            },
            'nAddressProblems': {
                'Value':'{0:1.0f}'.format(nAddressProblems), 
                'Label':'Address Problems'
            },
            'nNoisy2Pixel': {
                'Value':'{0:1.0f}'.format(nNoisy2Pixel), 
                'Label':'Noisy Pixels 2'
            },
            'nThrDefect': {
                'Value':'{0:1.0f}'.format(nThrDefect), 
                'Label':'Trim Problems'
            },
            'nGainDefect': {
                'Value':'{0:1.0f}'.format(nGainDefect), 
                'Label':'PH Gain defects'
            },
            'nPedDefect': {
                'Value':'{0:1.0f}'.format(nPedDefect), 
                'Label':'PH Pedestal defects'
            },
            'nPar1Defect': {
                'Value':'{0:1.0f}'.format(nPar1Defect), 
                'Label':'PH Parameter1 Defects'
            },
        }
        self.ResultData['KeyList'] = ['Total','nDeadPixel','nNoisy1Pixel','nMaskDefect','nDeadBumps','nDeadTrimbits','nAddressProblems','nNoisy2Pixel','nThrDefect','nGainDefect','nPedDefect','nPar1Defect']
    
