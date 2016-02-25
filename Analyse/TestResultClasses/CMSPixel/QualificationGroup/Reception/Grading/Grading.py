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
            'DefectiveBumps': {
                'Value': '-',
                'Label':'Bump Defects'
            },
            'DefectiveBumpsMax': {
                'Value': '-',
                'Label':'Max BumpDef/ROC'
            },
            'DeadPixels': {
                'Value': '-',
                'Label':'Dead Pixels'
            },
            'DeadPixelsMax': {
                'Value': '-',
                'Label':'Max Dead Pixels/ROC'
            },
            'Readback': {
                'Value': '-',
                'Label':'Readback calibration'
            },
            'Defects': {
                'Value': '',
                'Label':'Total Pixel defects'
            },
        }

        self.ResultData['KeyList'] = ['Module', 'Grade', 'DeadPixels', 'DefectiveBumps', 'DefectiveBumpsMax', 'DeadPixelsMax', 'Readback']

    def OpenFileHandle(self):

        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        NumBumpBondingProblems = []
        NumDeadPixels = []
        NumDefects = []
        PixelDefectsGrades = []
        Incomplete = False
        for i in chipResults:
            try:
                PixelDefectsGrade = int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'])
                NumBumpBondingProblems.append(int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefectiveBumps']))
                NumDeadPixels.append(int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDeadPixels']))
                NumDefects.append(int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefects']))
            except:
                Incomplete = True
                PixelDefectsGrade = 3
            PixelDefectsGrades.append(PixelDefectsGrade)

        try:
            ReadbackStatus = self.ParentObject.ResultData['SubTestResults']['ReadbackStatus'].ResultData['KeyValueDictPairs']['ModuleCalibrationGood']['Value']
        except:
            ReadbackStatus = "unknown"

        GradeMapping = {1:'A', 2:'B', 3:'C'}
        try:
            Grade = GradeMapping[max(PixelDefectsGrades)]
        except:
            Grade = 'None'

        self.ResultData['KeyValueDictPairs']['Module']['Value'] = self.ParentObject.Attributes['ModuleID']
        self.ResultData['KeyValueDictPairs']['Grade']['Value'] = Grade
        self.ResultData['KeyValueDictPairs']['DefectiveBumps']['Value'] = sum(NumBumpBondingProblems)
        self.ResultData['KeyValueDictPairs']['DefectiveBumpsMax']['Value'] = max(NumBumpBondingProblems)
        self.ResultData['KeyValueDictPairs']['DeadPixels']['Value'] = sum(NumDeadPixels)
        self.ResultData['KeyValueDictPairs']['DeadPixelsMax']['Value'] = max(NumDeadPixels)
        self.ResultData['KeyValueDictPairs']['Readback']['Value'] = ReadbackStatus
        self.ResultData['KeyValueDictPairs']['Defects']['Value'] = sum(NumDefects)

        self.ResultData['HiddenData']['ROCsLessThanOnePercent'] = len([x for x in PixelDefectsGrades if x == 1])
        self.ResultData['HiddenData']['ROCsMoreThanOnePercent'] = len([x for x in PixelDefectsGrades if x == 2])
        self.ResultData['HiddenData']['ROCsMoreThanFourPercent'] = len([x for x in PixelDefectsGrades if x == 3])

        if Incomplete:
            self.ResultData['KeyValueDictPairs']['Incomplete'] = {
                    'Value': 'INCOMPLETE',
                    'Label':'Test'
                }
            self.ResultData['KeyList'].append('Incomplete')

    def PopulateResultData(self):
        pass
