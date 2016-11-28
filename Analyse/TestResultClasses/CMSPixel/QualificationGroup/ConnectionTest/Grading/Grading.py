import AbstractClasses
import ROOT
import os

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
            'Comment': {
                'Value': '',
                'Label':'Comment'
            },
        }

        self.ResultData['KeyList'] = ['Module', 'Grade', 'ManualGrade']

    def splitSignalLevelString(self, signalLevelString):
        return [float(x.strip().split(' ')[0]) for x in signalLevelString.split('=')[1:]]

    def isSignalSymmetric(self, signalLevels):
        thr = abs(signalLevels[2])*0.15
        if thr < 40:
            thr = 40
        if (abs(abs(signalLevels[0])-abs(signalLevels[1])) > thr):
            print "asymetric signal levels:", signalLevels, thr
            return False
        return True

    def isSignalAmplitudeGood(self, signalLevels):
        if signalLevels[2] > 80:
            return True
        else:
            return False

    def OpenFileHandle(self):

        ElectricalGrade = 1
        Incomplete = False
        GradingComments = []

        try:
            # signal levels
            signalLevels = self.splitSignalLevelString(
                self.ParentObject.ResultData['SubTestResults']['SignalTest'].ResultData['KeyValueDictPairs'][
                'signal_clk']['Value'])

            if not self.isSignalAmplitudeGood(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("CLK amplitude too low")
            elif not self.isSignalSymmetric(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("CLK asymetric")

            signalLevels = self.splitSignalLevelString(
                self.ParentObject.ResultData['SubTestResults']['SignalTest'].ResultData['KeyValueDictPairs'][
                'signal_ctr']['Value'])

            if not self.isSignalAmplitudeGood(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("CTR amplitude too low")
            elif not self.isSignalSymmetric(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("CTR asymetric")

            signalLevels = self.splitSignalLevelString(
                self.ParentObject.ResultData['SubTestResults']['SignalTest'].ResultData['KeyValueDictPairs'][
                'signal_sda']['Value'])

            if not self.isSignalAmplitudeGood(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("SDA amplitude too low")
            elif not self.isSignalSymmetric(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("SDA asymetric")

            signalLevels = self.splitSignalLevelString(
                self.ParentObject.ResultData['SubTestResults']['SignalTest'].ResultData['KeyValueDictPairs'][
                'signal_sdata1']['Value'])

            if not self.isSignalAmplitudeGood(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("SDATA1 amplitude too low")
            elif not self.isSignalSymmetric(signalLevels):
                ElectricalGrade = 3
                GradingComments.append("SDATA1 asymetric")

            if self.ParentObject.Attributes['ModuleID'].startswith('M1'):
                signalLevels = self.splitSignalLevelString(
                    self.ParentObject.ResultData['SubTestResults']['SignalTest'].ResultData['KeyValueDictPairs'][
                    'signal_sdata2']['Value'])

                if not self.isSignalAmplitudeGood(signalLevels):
                    ElectricalGrade = 3
                    GradingComments.append("SDATA2 amplitude too low")
                elif not self.isSignalSymmetric(signalLevels):
                    ElectricalGrade = 3
                    GradingComments.append("SDATA2 asymetric")
        except:
            ElectricalGrade = 3
            GradingComments.append("INCOMPLETE: signal levels missing")

        # program ROC
        try:
            nProgrammableROCs = int(self.ParentObject.ResultData['SubTestResults']['ProgramROC'].ResultData['KeyValueDictPairs']['RocsProgrammable']['Value'])
            if nProgrammableROCs != self.ParentObject.Attributes['NumberOfChips']:
                GradingComments.append("not programmable!")
                ElectricalGrade = 3
        except:
            GradingComments.append("programROC test failed")
            ElectricalGrade = 3


        # IV grading
        IVGrade = 1

        # check if leakage current file exists
        LeakageCurrentFileName = self.RawTestSessionDataPath + '/../logfiles/IV.log'
        LeakageCurrentLines = []
        if os.path.isfile(LeakageCurrentFileName):
            with open(LeakageCurrentFileName, 'r') as LeakageCurrentFile:
                LeakageCurrentLines = [x for x in LeakageCurrentFile.readlines() if not x.strip().startswith('#')]
        if len(LeakageCurrentLines) > 0:

            try:
                IVRecalculated = float(self.ParentObject.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['I150Recalculated']['Value'])
            except:
                IVRecalculated = -1
                print "INCOMPLETE: NO IV!"
                Incomplete = True

            if IVRecalculated >= float(self.TestResultEnvironmentObject.GradingParameters['OnShellQuickTest_LeakageCurrent_C']):
                IVGrade = 3
                GradingComments.append("HIGH LEAKAGE CURRENT!")
            elif IVRecalculated >= float(self.TestResultEnvironmentObject.GradingParameters['OnShellQuickTest_LeakageCurrent_B']):
                IVGrade = 2
                GradingComments.append("little high leakage current")

            if IVRecalculated < 0.05:
                IVGrade = 3
                GradingComments.append("NO HV BIAS!")
                print "WARNING: NO HV! => graded C"
        else:
            print "WARNING: NO IV logfile found => ignored!!!!!"


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

        self.ResultData['KeyValueDictPairs']['Module']['Value'] = self.ParentObject.Attributes['ModuleID']
        self.ResultData['KeyValueDictPairs']['Grade']['Value'] = Grade

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
