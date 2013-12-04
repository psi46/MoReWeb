# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Summary1_TestResult'
        self.NameSingle='Summary1'
        self.Title = 'Summary 1'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        

    def getNumberOfRocsWithGrade(self,grade,gradeList):
        l = [i for i in gradeList if i == grade]
        return len(l)
    
    def PopulateResultData(self):
        subgradings = {}
        Grade = 1 # 1 = A, 2 = B, 3 = C 
        GradeMapping = {
            1:'A',
            2:'B',
            3:'C'
        }
        BadRocs = 0
        DeadPixels = 0
        AddressProblems = 0
        ThresholdDefects = 0
        MaskDefects = 0
        DeadBumps = 0
        NoisyPixels = 0
        TrimProblems = 0
        PHGainDefects = 0
        PHPedestalDefects = 0
        PHPar1Defects = 0
        TotalDefects = 0
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        for i in chipResults:
            if int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value']) > 0.01 * 52*80:
                BadRocs += 1
            DeadPixels += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadPixel']['Value'])
            AddressProblems += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nAddressProblems']['Value'])
            ThresholdDefects += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value'])
            MaskDefects += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nMaskDefect']['Value'])
            DeadBumps += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadBumps']['Value'])
            NoisyPixels += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nNoisy1Pixel']['Value'])
            TrimProblems += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value'])
            PHGainDefects += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nGainDefect']['Value'])
            PHPedestalDefects += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPedDefect']['Value'])
            PHPar1Defects += int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPar1Defect']['Value'])
            TotalDefects +=int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value'])
        subgradings['PixelDefects'] =  [ i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'] for i in chipResults]
       
        # Grading
        
        for i in ['Noise', 'VcalThresholdWidth', 'RelativeGainWidth', 'PedestalSpread', 'Parameter1']:
            if not self.ParentObject.ResultData['SubTestResults'].has_key(i):
                continue
            TestResultObject = self.ParentObject.ResultData['SubTestResults'][i]
            subgrading = []
            for j in range(self.ParentObject.Attributes['NumberOfChips']-self.ParentObject.Attributes['StartChip']):
            
                Value= TestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(j+1) 
                nValue = TestResultObject.ResultData['Plot']['ROOTObject_h2'].GetBinContent(j+1) 
                
                
                # Grading 
                grade = 1
                if Value  < TestResultObject.ResultData['HiddenData']['LimitB']:
                    grade = 1
                elif Value  < TestResultObject.ResultData['HiddenData']['LimitC']:
                    grade = 2
                else:
                    grade = 3
                if grade == 1 and nValue < (4160 - self.TestResultEnvironmentObject.GradingParameters['defectsB']):
                    grade = 2
                if nValue < (4160 - self.TestResultEnvironmentObject.GradingParameters['defectsC']):
                    grade = 3
                subgrading.append('%d'%grade)
                    
                if Grade == 1 and Value > TestResultObject.ResultData['HiddenData']['LimitB']:
                    Grade = 2
                if Value > TestResultObject.ResultData['HiddenData']['LimitC']:
                    Grade = 3
                if Grade == 1 and nValue < (4160 - self.TestResultEnvironmentObject.GradingParameters['defectsB']):
                    Grade = 2
                if nValue < (4160 - self.TestResultEnvironmentObject.GradingParameters['defectsC']):
                    Grade = 3
                '''
                # Failures reasons...
                if Value > criteriaB[i] and Value < criteriaC[i]:
                    fitsProblemB[i]++
                if Value > criteriaC[i]:
                    fitsProblemC[i]++
                '''
#             print '%s: %s'%(i,subgrading)
            subgradings[i] = subgrading
        CurrentAtVoltage150 = 0
        CurrentVariation = 0
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            IVTestResult = self.ParentObject.ResultData['SubTestResults']['IVCurve']    
            CurrentAtVoltage150 = float(IVTestResult.ResultData['KeyValueDictPairs']['CurrentAtVoltage150']['Value'])
            CurrentVariation = float(IVTestResult.ResultData['KeyValueDictPairs']['Variation']['Value'])
        else:
            pass
        for i in subgradings:
            print '%s: %s/%s/%s'%(i,self.getNumberOfRocsWithGrade('1',subgradings[i]),self.getNumberOfRocsWithGrade('2',subgradings[i]),self.getNumberOfRocsWithGrade('3',subgradings[i]))
            
#         print 'PixelDefects: %s'%subgradings['PixelDefects']
#         print 'A:',self.getNumberOfRocsWithGrade('1',subgradings['PixelDefects'])
#         print 'B:',self.getNumberOfRocsWithGrade('2',subgradings['PixelDefects'])
#         print 'C:',self.getNumberOfRocsWithGrade('3',subgradings['PixelDefects'])        
        #TODO
        if self.ParentObject.Attributes['TestType']  == 'p17_1':
            # Grading
            if Grade == 1 and BadRocs > 1:
                Grade = 2
            if Grade == 1 and CurrentAtVoltage150 > self.TestResultEnvironmentObject.GradingParameters['currentB']:
                    
                Grade = 2;
            if Grade == 1   and CurrentVariation >  self.TestResultEnvironmentObject.GradingParameters['slopeivB']:
                    
                Grade = 2
            if BadRocs > 2:
                Grade = 3
            if CurrentAtVoltage150 > self.TestResultEnvironmentObject.GradingParameters['currentC']:
                Grade = 3; 

            '''
            // Failures reasons...
            if( (i150> currentB) && (i150 < currentC) ) currentProblemB++;
            if( (i150> currentC) ) currentProblemC++;
            if( (ratio > slopeivB) ) slopeProblemB++;
 '''
        else:   
            # Grading
            if Grade == 1 and BadRocs > 1:
                Grade = 2
            if Grade == 1 and CurrentAtVoltage150 > self.TestResultEnvironmentObject.GradingParameters['currentBm10']:
                Grade = 2
            if Grade == 1 and CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivB']:
                Grade = 2
            if BadRocs > 2:
                Grade = 3
            if CurrentAtVoltage150 > self.TestResultEnvironmentObject.GradingParameters['currentCm10']:
                Grade = 3
                
            '''
            # Failures reasons...
            if (i150> 1.5*currentB and i150 < 1.5*currentC)currentProblemB++;
            if (i150> 1.5*currentC) ){ currentProblemC++;}
            if (ratio > slopeivB) ){ slopeProblemB++;}
            '''
            
            
        
        nPixelDefectsTotal  = 0
        nPixelDefectsGradeA = self.getNumberOfRocsWithGrade('1',subgradings['PixelDefects'])
        nPixelDefectsGradeB = self.getNumberOfRocsWithGrade('2',subgradings['PixelDefects'])
        nPixelDefectsGradeC = self.getNumberOfRocsWithGrade('3',subgradings['PixelDefects'])
        
        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'], 
                'Label':'Module'
            },
            'Grade': {
                'Value':GradeMapping[Grade], 
                'Label':'Grade'
            },
            'BadRocs': {
                'Value':'{0:1.0f}'.format(BadRocs), 
                'Label':'ROCs > 1% defects'
            },
            'DeadPixels': {
                'Value':'{0:1.0f}'.format(DeadPixels), 
                'Label':'Dead Pixels'
            },
            'AddressProblems': {
                'Value':'{0:1.0f}'.format(AddressProblems), 
                'Label':'Address Problems'
            },
            'ThresholdDefects': {
                'Value':'{0:1.0f}'.format(ThresholdDefects), 
                'Label':'Threshold Defects'
            },
            'PixelDefects': {
                'Value':'%d - %d/%d/%d'%(TotalDefects,nPixelDefectsGradeA,nPixelDefectsGradeB,nPixelDefectsGradeC),
                'Label':'Pixel Defects - A/B/C'
            },
            'MaskDefects':{
                'Value':'{0:1.0f}'.format(MaskDefects), 
                'Label':'Mask Defects'
            },
            'DeadBumps':{
                'Value':'{0:1.0f}'.format(DeadBumps), 
                'Label':'Dead Bumps'
            },
            'NoisyPixels':{
                'Value':'{0:1.0f}'.format(NoisyPixels), 
                'Label':'Noisy Pixels'
            },
            'TrimProblems':{
                'Value':'{0:1.0f}'.format(TrimProblems), 
                'Label':'Trim Problems'
            },
            'PHGainDefects':{
                'Value':'{0:1.0f}'.format(PHGainDefects), 
                'Label':'PH Gain Defects'
            },
            'PHPedestalDefects':{
                'Value':'{0:1.0f}'.format(PHPedestalDefects), 
                'Label':'PH Pedestal Defects'
            },
            'PHPar1Defects':{
                'Value':'{0:1.0f}'.format(PHPar1Defects), 
                'Label':'PH Parameter1 Defects'
            },
        }
        for i in subgradings:
            for grade in GradeMapping:
                key = i+'Grade'+GradeMapping[grade]+"ROCs"
                nRocs = self.getNumberOfRocsWithGrade('%d'%grade,subgradings[i])
                entry = {
                    'Value': nRocs,
                    'Label': '%s grade %s ROCs'%(i,GradeMapping[grade])
                }
                print key, entry
                self.ResultData['KeyValueDictPairs'][key] = entry
        self.ResultData['KeyList'] = ['Module','Grade','PixelDefects', 'DeadPixels','AddressProblems', 'ThresholdDefects', 'MaskDefects', 'DeadBumps', 'NoisyPixels', 'TrimProblems', 'PHGainDefects', 'PHPedestalDefects', 'PHPar1Defects']

