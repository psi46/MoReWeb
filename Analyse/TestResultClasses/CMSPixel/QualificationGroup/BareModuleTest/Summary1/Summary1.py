# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Summary1_TestResult'
        self.NameSingle='Summary1'
        self.Title = 'Module Statistic'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        

    def getNumberOfRocsWithGrade(self,grade,gradeList):
        l = [i for i in gradeList if i == grade]
        return len(l)
    
    def PopulateResultData(self):

        DeadPixels = 0
        DeadBumps = 0
        MissingBumps = 0
        totalMissingBumps = 0
        totalDeadBumps = 0

        # obtain the values to get dispayed
        print 'Begin Summary1: ',self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        for i in chipResults:
            MissingBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['NMissingBumps']['Value']);
            totalMissingBumps = totalMissingBumps + MissingBumps;
            DeadBumps = int(i['TestResultObject'].ResultData['SubTestResults']['BareBBMap'].ResultData['KeyValueDictPairs']['NDeadBumps']['Value']);
            totalDeadBumps = totalDeadBumps + DeadBumps;
            print 'Inside Chips-loop:',i,MissingBumps,totalDeadBumps

        print 'totalMissingBumps: ',totalMissingBumps,totalDeadBumps
        self.ResultData['KeyValueDictPairs'] = {
            'NMissingBumps': {
                'Value':totalMissingBumps,
                'Label':'Total MissingBumps'
            },
            'NDeadBumps': {
                'Value':totalDeadBumps,
                'Label':'Total DeadBumps'
            },
        }


        self.ResultData['KeyList'] = ['NMissingBumps','NDeadBumps']
