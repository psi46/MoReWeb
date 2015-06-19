# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Summary1_TestResult'
        self.NameSingle='Summary1'
        self.Title = 'Summary 1'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        
    def PopulateResultData(self):
        GradeMapping = {
            1:'A',
            2:'B',
            3:'C'
        }
        BadRocs = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['BadRocs']['Value'])
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
        
        # Grading
        
        CurrentAtVoltage150V = 0
        CurrentVariation = 0
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            IVTestResult = self.ParentObject.ResultData['SubTestResults']['IVCurve']    
            CurrentAtVoltage150V = float(IVTestResult.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Value'])
            CurrentVariation = float(IVTestResult.ResultData['KeyValueDictPairs']['Variation']['Value'])
        else:
            pass


        
        nPixelDefectsTotal  = 0
        nPixelDefectsGradeA = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['nPixelDefectsGradeA']['Value'])
        nPixelDefectsGradeB = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['nPixelDefectsGradeB']['Value'])
        nPixelDefectsGradeC = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['nPixelDefectsGradeC']['Value'])
        ModuleGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Value'])
        
        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'], 
                'Label':'Module'
            },
            'Grade': {
                'Value':GradeMapping[ModuleGrade], 
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
                'Label':'Pixel Defects - A/B/C',
                'NumericValue':TotalDefects,
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
        self.ResultData['KeyList'] = ['Module','Grade','PixelDefects', 'DeadPixels','AddressProblems', 'ThresholdDefects', 'MaskDefects', 'DeadBumps', 'NoisyPixels', 'TrimProblems', 'PHGainDefects', 'PHPedestalDefects', 'PHPar1Defects']


	SubGradings = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGradings']
        
        # needed in summary3 and in fulltest db upload
        for i in SubGradings:
            for Grade in GradeMapping:
                key = i+'Grade'+GradeMapping[Grade]+"ROCs"
                self.ResultData['KeyValueDictPairs'][key] = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs'][key]
                
                # the following line would enable these subgradings in the summary table
		#self.ResultData['KeyList'].append(key)      
        
