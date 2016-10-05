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
            'ManualGrade': {
                'Value': '-',
                'Label':'Manual grade'
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
            'Comment': {
                'Value': '',
                'Label':'Comment'
            },
        }

        self.ResultData['KeyList'] = ['Module', 'Grade', 'ManualGrade', 'ElectricalGrade', 'IVGrade', 'DeadPixels', 'DefectiveBumps', 'DefectiveBumpsMax', 'DeadPixelsMax', 'Readback']

    def OpenFileHandle(self):

        # chip pixel defects grading
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        NumBumpBondingProblems = []
        NumDeadPixels = []
        NumDefects = []
        PixelDefectsGrades = []
        Incomplete = False
        GradingComments = []

        ChipIndex = 0
        for i in chipResults:
            try:
                PixelDefectsGrade = int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'])
                NumBumpBondingProblems.append(int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefectiveBumps']))
                NumDeadPixels.append(int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDeadPixels']))
                NumDefects.append(int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NDefects']))
            except:
                Incomplete = True
                print "Pixel tests missing C%d"%ChipIndex
                GradingComments.append("Pixel tests missing C%d"%ChipIndex)

            try:
                if not i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DefectsGradingComplete']:
                    Incomplete = True
                    GradingComments.append("Pixel tests incomplete C%d"%ChipIndex)
                    print "Pixel tests incomplete C%d"%ChipIndex
            except:
                Incomplete = True
                print "Pixel tests incomplete C%d" % ChipIndex

            PixelDefectsGrades.append(PixelDefectsGrade)
            ChipIndex += 1

        ElectricalGrade = max(PixelDefectsGrades)

        if 'IanaProblem' in self.ParentObject.ResultData['SubTestResults']['Logfile'].ResultData['HiddenData'] and self.ParentObject.ResultData['SubTestResults']['Logfile'].ResultData['HiddenData']['IanaProblem']:
            ElectricalGrade = 3

        # IV grading
        IVGrade = 1
        try:
            IVRecalculated = float(self.ParentObject.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['I150Recalculated']['Value'])
        except:
            IVRecalculated = -1
            print "INCOMPLETE: NO IV!"
            Incomplete = True

        if IVRecalculated >= float(self.TestResultEnvironmentObject.GradingParameters['OnShellQuickTest_LeakageCurrent_C']):
            IVGrade = 3
        elif IVRecalculated >= float(self.TestResultEnvironmentObject.GradingParameters['OnShellQuickTest_LeakageCurrent_B']):
            IVGrade = 2

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
            self.ResultData['HiddenData']['ModuleGrade'] = ModuleGrade
        except:
            Grade = 'None'
            self.ResultData['HiddenData']['ModuleGrade'] = -1


        # readback calibration flag
        try:
            ReadbackStatus = self.ParentObject.ResultData['SubTestResults']['ReadbackStatus'].ResultData['KeyValueDictPairs']['ModuleCalibrationGood']['Value']
        except:
            ReadbackStatus = "unknown"

        self.ResultData['KeyValueDictPairs']['Module']['Value'] = self.ParentObject.Attributes['ModuleID']
        self.ResultData['KeyValueDictPairs']['Grade']['Value'] = Grade
        self.ResultData['KeyValueDictPairs']['ElectricalGrade']['Value'] = GradeMapping[ElectricalGrade] if ElectricalGrade in GradeMapping else 'None'
        self.ResultData['KeyValueDictPairs']['IVGrade']['Value'] = GradeMapping[IVGrade] if IVGrade in GradeMapping else 'None'
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
                    'Label': 'Test',
                    'Style': 'color:red;font-weight:bold;'
                }
            self.ResultData['KeyList'].append('Incomplete')

        if len(GradingComments) > 0:
            self.ResultData['KeyValueDictPairs']['Comment']['Value'] = '; '.join(GradingComments)
            self.ResultData['KeyList'].append('Comment')

    def PopulateResultData(self):
        pass
