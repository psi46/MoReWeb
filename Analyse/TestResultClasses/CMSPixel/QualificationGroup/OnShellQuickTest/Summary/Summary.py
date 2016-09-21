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

        self.ResultData['KeyList'] = ['Module', 'Grade', 'ElectricalGrade', 'IVGrade', 'DeadPixels', 'DefectiveBumps', 'Comment']

    def OpenFileHandle(self):

        Incomplete = False
        ElectricalGrade = 1
        IVGrade = 1
        GradingComments = []

        # chip pixel defects grading
        # Final Grade
        # translate grade from number to A/B/C
        GradeMapping = {1:'A', 2:'B', 3:'C'}

        ModuleGrade = max(ElectricalGrade, IVGrade)

        # Grade C if incomplete
        if Incomplete:
            ModuleGrade = 3

        # manual Grade
        ManualGrade = self.check_for_manualGrade()
        if ManualGrade != '':
            self.ResultData['KeyValueDictPairs']['ManualGrade']['Value'] = str(GradeMapping[int(ManualGrade)])
            if GradeMapping[ModuleGrade] != GradeMapping[int(ManualGrade)]:
                GradeComment = "Grade "+str(GradeMapping[ModuleGrade])+" -> "+str(GradeMapping[int(ManualGrade)])
                print GradeComment
                GradingComments.append(GradeComment)
            ModuleGrade = int(ManualGrade)

        try:
            Grade = GradeMapping[ModuleGrade]
        except:
            Grade = 'None'

        # readback calibration flag
        try:
            ReadbackStatus = self.ParentObject.ResultData['SubTestResults']['ReadbackStatus'].ResultData['KeyValueDictPairs']['ModuleCalibrationGood']['Value']
        except:
            ReadbackStatus = "unknown"

        self.ResultData['KeyValueDictPairs']['Module']['Value'] = self.ParentObject.Attributes['ModuleID']
        self.ResultData['KeyValueDictPairs']['Grade']['Value'] = Grade
        self.ResultData['KeyValueDictPairs']['ElectricalGrade']['Value'] = GradeMapping[ElectricalGrade] if ElectricalGrade in GradeMapping else 'None'
        self.ResultData['KeyValueDictPairs']['IVGrade']['Value'] = GradeMapping[IVGrade] if IVGrade in GradeMapping else 'None'

        if Incomplete:
            self.ResultData['KeyValueDictPairs']['Incomplete'] = {
                    'Value': 'INCOMPLETE',
                    'Label': 'Test',
                    'Style': 'color:red;font-weight:bold;'
                }
            self.ResultData['KeyList'].append('Incomplete')

        if len(GradingComments) > 0:
            self.ResultData['KeyValueDictPairs']['Comment']['Value'] = '; '.join(GradingComments)
            self.ResultData['KeyList'].append('Comment')

    def PopulateResultData(self):
        pass
