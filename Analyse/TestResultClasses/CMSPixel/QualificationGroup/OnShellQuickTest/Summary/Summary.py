import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Grading_Chips_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = None
        self.Title = 'Summary'

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value': '',
                'Label':'Module'
            },
            'Grade': {
                'Value': '-',
                'Label':'Grade'
            },
            'ElectricalGrade': {
                'Value': '-',
                'Label':'Electrical Grade'
            },
            'IVGrade': {
                'Value': '-',
                'Label':'IV Grade'
            },
            'ManualGrade': {
                'Value': '-',
                'Label':'Manual Grade'
            },
            'DefectiveBumps': {
                'Value': '-',
                'Label':'Bump Defects'
            },
            'DeadPixels': {
                'Value': '-',
                'Label':'Dead Pixels'
            },
            'Defects': {
                'Value': '',
                'Label':'Total Pixel defects'
            },
            'Comment': {
                'Value': '',
                'Label':'Comment'
            },
        }

        self.ResultData['KeyList'] = ['Module', 'Grade', 'ElectricalGrade', 'ManualGrade', 'IVGrade', 'DeadPixels', 'DefectiveBumps', 'Comment']

    def OpenFileHandle(self):

        Grade = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['Grade']['Value']
        ElectricalGrade = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ElectricalGrade']['Value']
        IVGrade = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['IVGrade']['Value']
        ManualGrade = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ManualGrade']['Value'] if 'ManualGrade' in self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs'] else '-'

        self.ResultData['KeyValueDictPairs']['Module']['Value'] = self.ParentObject.Attributes['ModuleID']
        self.ResultData['KeyValueDictPairs']['Grade']['Value'] = Grade
        self.ResultData['KeyValueDictPairs']['ElectricalGrade']['Value'] = ElectricalGrade
        self.ResultData['KeyValueDictPairs']['IVGrade']['Value'] = IVGrade
        self.ResultData['KeyValueDictPairs']['ManualGrade']['Value'] = ManualGrade

        self.ResultData['KeyValueDictPairs']['DefectiveBumps']['Value'] = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['DefectiveBumps']['Value']
        self.ResultData['KeyValueDictPairs']['DeadPixels']['Value'] = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        self.ResultData['KeyValueDictPairs']['Defects']['Value'] = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['Defects']['Value']

        if 'Incomplete' in self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']:
            self.ResultData['KeyValueDictPairs']['Incomplete'] = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['Incomplete']
            self.ResultData['KeyList'].append('Incomplete')

    def PopulateResultData(self):
        pass
