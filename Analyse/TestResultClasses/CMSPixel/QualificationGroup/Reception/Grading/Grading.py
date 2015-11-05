import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Grading_Chips_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = None
        self.Title = 'Summary'

    def OpenFileHandle(self):

        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        NumBumpBondingProblems = []
        NumDeadPixels = []
        for i in chipResults:
            NumBumpBondingProblems.append(int(i['TestResultObject'].ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['nBumpBondingProblems']['Value']))
            NumDeadPixels.append(int(i['TestResultObject'].ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['NDeadPixels']['Value']))


        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'], 
                'Label':'Module'
            },
            'DefectiveBumps': {
                'Value': sum(NumBumpBondingProblems),
                'Label':'Bump Defects'
            },
            'DefectiveBumpsMax': {
                'Value': max(NumBumpBondingProblems),
                'Label':'Max BumpDef/ROC'
            },
            'DeadPixels': {
                'Value': sum(NumDeadPixels),
                'Label':'Dead Pixels'
            },
            'DeadPixelsMax': {
                'Value': max(NumDeadPixels),
                'Label':'Max Dead Pixels/ROC'
            },
        }
        self.ResultData['KeyList'] = ['Module', 'DeadPixels', 'DefectiveBumps', 'DefectiveBumpsMax', 'DeadPixelsMax']

    def PopulateResultData(self):
        pass
