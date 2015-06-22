# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Grading_TestResult'
        self.NameSingle = 'Grading'
        self.Title = 'Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'


    def getNumberOfRocsWithGrade(self, Grade, GradeList):
        l = [i for i in GradeList if i == Grade]
        return len(l)


    def PopulateResultData(self):
        SubGradings = {}
        ModuleGrade = 1
        GradeMapping = {
            1: 'A',
            2: 'B',
            3: 'C'
        }
        BadRocs = 0
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
       
        GradeHistogram = {
            'A': 0,
            'B': 0,
            'C': 0,
        }
        SubGrading = []
        for i in chipResults:
            ROCGrade = i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrade']['Value']
            GradeHistogram[ROCGrade] += 1
            if ROCGrade == GradeMapping[2] and ModuleGrade < 2:
                ModuleGrade = 2
            if ROCGrade == GradeMapping[3] and ModuleGrade < 3:
                ModuleGrade = 3


        SubGradings['PixelDefects'] = SubGrading
        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value': self.ParentObject.Attributes['ModuleID'],
                'Label': 'Module'
            },
            'ModuleGrade': {
                'Value': GradeMapping[ModuleGrade],
                'Label': 'Grade'
            },
            'ROCGrades': {
                'Value': '%d/%d/%d'%(GradeHistogram['A'], GradeHistogram['B'], GradeHistogram['C']),
                'Label': 'ROC Grades A/B/C'
            },
        }
        self.ResultData['HiddenData']['SubGradings'] = SubGradings
        self.ResultData['KeyList'] = ['Module', 'ModuleGrade', 'ROCGrades']


        # needed in summary1
        if self.verbose:
            print 'SubGradings of ROCs:'
        for i in SubGradings:
            for Grade in GradeMapping:
                key = i + 'Grade' + GradeMapping[Grade] + "ROCs"
                try:
                    nRocs = self.getNumberOfRocsWithGrade('%d' % Grade, SubGradings[i])
                except:
                    nRocs = -1
                entry = {
                    'Value': nRocs,
                    'Label': '%s Grade %s ROCs' % (i, GradeMapping[Grade])
                }
                if self.verbose:
                    print key, entry
                self.ResultData['KeyValueDictPairs'][key] = entry



