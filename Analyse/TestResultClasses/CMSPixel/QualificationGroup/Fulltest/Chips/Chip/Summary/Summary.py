import AbstractClasses

try:
       set
except NameError:
       from sets import Set as set

def defectsListLength(defectsList):
    if defectsList is not None:
        return "%d"%len(defectsList)
    else:
        return '#'

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):

    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_Summary_TestResult'
        self.NameSingle = 'Summary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        
    # grading and related functions (HasBumpBondingProblems, etc.) moved to Grading.py
    def PopulateResultData(self):

        self.ResultData['KeyValueDictPairs'] = {
            'Total': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['TotalList']),
                'Label':'Total'
            },
            'nDeadPixel': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadPixelList']),
                'Label':' - Dead Pixels'
            },
            'nNoisy1Pixel': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Noisy1PixelList']),
                'Label':'>100% efficiency in alive map'
            },
            'nMaskDefect': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['MaskDefectList']),
                'Label':' - Mask Defects'
            },
            'nDeadBumps': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadBumpList']),
                'Label':' - Dead Bumps %s'%(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SpecialBumpBondingTestName'] if self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData'].has_key('SpecialBumpBondingTestName') else '') 
            },
            'nDeadTrimbits': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadTrimbitsList']),
                'Label':' - Dead Trimbits'
            },
            'nAddressProblems': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['AddressProblemList']),
                'Label':' - Address Problems'
            },
            'nNoisy2Pixel': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NoiseDefectList']),
                'Label':'Noisy Pixels'
            },
            'nThrDefect': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['ThrDefectList']),
                'Label':'Trim Problems'
            },
            'nGainDefect': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['GainDefectList']),
                'Label':'PH Gain defects'
            },
            'nPedDefect': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['PedDefectList']),
                'Label':'PH Pedestal defects'
            },
            'nPar1Defect': {
                'Value': defectsListLength(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Par1DefectList']),
                'Label':'PH Parameter1 Defects'
            },
            'PixelDefectsGrade':{
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'],
                'Label': 'Pixel Defects Grade ROC'
            },
            'empty':{
                'Value': '',
                'Label': ''
            }
        }
        self.ResultData['KeyList'] = ['Total', 'nDeadPixel', 'nMaskDefect', 'nDeadBumps', 'nDeadTrimbits', 'nAddressProblems', 'empty',
                                      'nNoisy1Pixel', 'nNoisy2Pixel', 'nThrDefect', 'nGainDefect', 'nPedDefect', 'nPar1Defect', 'PixelDefectsGrade']

