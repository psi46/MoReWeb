# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Summary_TestResult'
        self.NameSingle='XRayHRQualification'
        self.Title = 'Summary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        
    def PopulateResultData(self):
        GradeMapping = {
            1:'A',
            2:'B',
            3:'C'
        }

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'], 
                'Label':'Module'
            },
            'Grade': {
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Value'],
                'Label': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Label']
            },
            'ROCGrades': {
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrades']['Value'],
                'Label': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrades']['Label']
            }
        }
        self.ResultData['KeyList'] = ['Module','Grade', 'ROCGrades']

