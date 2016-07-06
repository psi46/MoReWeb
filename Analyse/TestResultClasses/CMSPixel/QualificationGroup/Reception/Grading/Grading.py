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
                GradingComments.append("Pixel tests missing C%d"%ChipIndex)

            if not i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DefectsGradingComplete']:
                Incomplete = True
                GradingComments.append("Pixel tests incomplete C%d"%ChipIndex)

            PixelDefectsGrades.append(PixelDefectsGrade)
            ChipIndex += 1

        ElectricalGrade = max(PixelDefectsGrades)

        # IV Grading
        IVGrade = 0
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            IVGrade = 1
            IVTestResult = self.ParentObject.ResultData['SubTestResults']['IVCurve']
            CurrentAtVoltage150V = float(IVTestResult.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Value'])
            CurrentVariation = float(IVTestResult.ResultData['KeyValueDictPairs']['Variation']['Value'])

            # current
            #    grading is done with the measured value at +17
            if IVGrade == 1 and CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentB']:
                IVGrade = 2
            if CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentC']:
                IVGrade = 3

            # slope
            #    grading is only done with the measured value at +17
            if IVGrade == 1 and CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivB']:
                IVGrade = 2
            if CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivC']:
                IVGrade = 3

            if ('IVCurveFilePath' not in IVTestResult.ResultData['HiddenData']) or len(IVTestResult.ResultData['HiddenData']['IVCurveFilePath'].strip()) < 1:
                IVGrade = 0
                Incomplete = True
                GradingComments.append("IV curve logfile missing")
        else:
            Incomplete = True
            GradingComments.append("IV subtest folder missing")

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
