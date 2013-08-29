import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_Summary_TestResult'
        self.NameSingle='Summary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        nDeadPixel = 0
        nIneffPixel = 0
        nMaskDefect = 0
        nNoisy1Pixel = 0
        nDeadBumps = 0
        nDeadTrimbits = 0
        nAddressProblems = 0
    
        nNoisy2Pixel = 0
        nThrDefect = 0
        nGainDefect = 0
        nPedDefect = 0
        nPar1Defect = 0
    
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
            
        for i in range(52): #Column
            for j in range(80): #Row
                
                pixel_alive   = 1
                px_funct_counted = 0
                px_perf_counted = 0
                px_counted = 0
        
                trim_counted = 0
                ph_counted = 0
        
                PixelMapCurrentValue = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['Plot']['ROOTObject'].GetBinContent(i+1, j+1)
                
                # -- Pixel alive
                if  PixelMapCurrentValue == 0:
                    
                    pixel_alive = 0
                    nDeadPixel += 1
                elif PixelMapCurrentValue  > self.TestResultEnvironmentObject.GradingParameters['PixelMapMaxValue']:
                    nNoisy1Pixel += 1
                    px_counted = 1 
                    px_funct_counted = 1
                elif PixelMapCurrentValue  < self.TestResultEnvironmentObject.GradingParameters['PixelMapMinValue']:
                    nMaskDefect += 1  
                    px_counted = 1
                    px_funct_counted = 1
                else:
                    nIneffPixel += 1
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
                    except (ValueError, TypeError, IndexError):
                        pass    
        
        Total = nDeadPixel + nMaskDefect + nDeadTrimbits + nAddressProblems
        
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
    
