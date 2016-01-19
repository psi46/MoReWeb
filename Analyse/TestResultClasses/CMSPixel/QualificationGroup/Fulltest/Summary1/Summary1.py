# -*- coding: utf-8 -*-
import AbstractClasses

def decode_chip_pixel_defects(d):
    try:
        return int(d)
    except:
        return 0

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
            DeadPixels += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadPixel']['Value'])
            AddressProblems += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nAddressProblems']['Value'])
            ThresholdDefects += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value'])
            MaskDefects += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nMaskDefect']['Value'])
            DeadBumps += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadBumps']['Value'])
            NoisyPixels += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nNoisy2Pixel']['Value'])
            TrimProblems += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadTrimbits']['Value'])
            PHGainDefects += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nGainDefect']['Value'])
            PHPedestalDefects += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPedDefect']['Value'])
            PHPar1Defects += decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPar1Defect']['Value'])
            TotalDefects +=decode_chip_pixel_defects(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value'])
        
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
        try:
            PixelDefectsRocsA = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsRocsA']['Value'])
        except:
            PixelDefectsRocsA = -1
        try:
            PixelDefectsRocsB = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsRocsB']['Value'])
        except:
            PixelDefectsRocsB = -1
        try:
            PixelDefectsRocsC = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsRocsC']['Value'])
        except:
            PixelDefectsRocsC = -1

        ModuleGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Value'])
        ElectricalGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ElectricalGrade']['Value'])
        IVGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['IVGrade']['Value'])
        ManualGrade = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ManualGrade']['Value']) if 'ManualGrade' in self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs'] else 0

        GradeText = GradeMapping[ModuleGrade] if ModuleGrade in GradeMapping else 'None'

        if self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData'].has_key('MissingSubtests') and int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['MissingSubtests']['Value'])>0:
            StatusText = 'INCOMPLETE'
            StatusStyle = 'color:red;font-weight:bold;'
        else:
            StatusText = 'OK'
            StatusStyle = ''

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'], 
                'Label':'Module'
            },
            'Grade': {
                'Value': GradeText,
                'Label':'Grade'
            },
            'Status': {
                'Value': StatusText,
                'Label':'Status',
                'Style': StatusStyle
            },
            'ElectricalGrade': {
                'Value': GradeMapping[ElectricalGrade] if ElectricalGrade in GradeMapping else 'None',
                'Label':'Electrical Grade'
            },
            'IVGrade': {
                'Value':GradeMapping[IVGrade] if IVGrade in GradeMapping else 'None',
                'Label':'IV Grade'
            },
            'ManualGrade': {
                'Value':GradeMapping[ManualGrade] if ManualGrade in GradeMapping else 'None',
                'Label':'Manual Grade'
            },
            'PixelDefectsRocsA': {
                'Value':'{0:1.0f}'.format(PixelDefectsRocsA), 
                'Label':'ROCs < 1% defects'
            },
            'PixelDefectsRocsB': {
                'Value':'{0:1.0f}'.format(PixelDefectsRocsB), 
                'Label':'ROCs > 1% defects'
            },
            'PixelDefectsRocsC': {
                'Value':'{0:1.0f}'.format(PixelDefectsRocsC), 
                'Label':'ROCs > 4% defects'
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
                'Value':'%d - %d/%d/%d'%(TotalDefects,PixelDefectsRocsA,PixelDefectsRocsB,PixelDefectsRocsC),
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
                'Label':'Noise Defects'
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
        self.ResultData['KeyList'] = ['Module','Grade']
        if StatusText != 'OK':
            self.ResultData['KeyList'].append('Status')

        self.ResultData['KeyList'] += ['ElectricalGrade', 'IVGrade', 'ManualGrade', 'PixelDefects', 'DeadPixels','AddressProblems', 'ThresholdDefects', 'MaskDefects', 'DeadBumps', 'NoisyPixels', 'TrimProblems', 'PHGainDefects', 'PHPar1Defects']

        SubGradings = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SubGradings']
        # needed in summary3 and in fulltest db upload
        for i in SubGradings:
            for Grade in GradeMapping:
                key = i+'Grade'+GradeMapping[Grade]+"ROCs"
                self.ResultData['KeyValueDictPairs'][key] = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs'][key]

                # the following line would enable these subgradings in the summary table
                #self.ResultData['KeyList'].append(key)