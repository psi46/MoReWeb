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
        if 'ManualGrade' in self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']:
            ManualGradeNumeric = int(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ManualGrade']['Value'])
            ManualGrade = GradeMapping[ManualGradeNumeric] if ManualGradeNumeric in GradeMapping else ''
        else:
            ManualGrade = ''

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'], 
                'Label':'Module'
            },
            'Grade': {
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Value'],
                'Label': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ModuleGrade']['Label']
            },
            'ManualGrade': {
                'Value': ManualGrade if ManualGrade else 'None',
                'Label': 'Manual Grade',
                'Style': 'font-weight:bold;' if ManualGrade else '',
            },
            'ROCGrades': {
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrades']['Value'],
                'Label': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrades']['Label']
            },
            'PixelDefects': {
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefects']['Value'],
                'Label': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefects']['Label']
            },
            'BumpBondingDefects': {
                'Value': "{BB:1.0f}".format(BB=self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['BumpBondingDefects']['Value']), 
                'Label': 'Bump Bonding Defects',
            },
            'NoisyPixels': {
                'Value': "{NoisyPixels:1.0f}".format(NoisyPixels=self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NoiseDefects']['Value']), 
                'Label': 'Noisy Pixels',
            },
            'HotPixelDefects': {
                'Value': "{HotPixelDefects:1.0f}".format(HotPixelDefects=self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['HotPixelDefects']['Value']), 
                'Label': 'Hot Pixels',
            },
            'ROCsWithReadoutProblems': {
                'Value': "{ROCsWithReadoutProblems:1.0f}".format(ROCsWithReadoutProblems=self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsWithReadoutProblems']['Value']), 
                'Label': 'ROCs with r/o problems',
            },
            'ROCsWithUniformityProblems': {
                'Value': "{ROCsWithUniformityProblems:1.0f}".format(ROCsWithUniformityProblems=self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCsWithUniformityProblems']['Value']), 
                'Label': 'ROCs with unif problems',
            },
        }

        ### Mean Efficiency ###
        RatesString = ''
        EfficienciesString = ''
        for Rate in self.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            RatesString = (RatesString + "/{Rate}".format(Rate=Rate)).strip("/")

            EfficiencyList = []
            for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                Efficiency = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Efficiency_{Rate}'.format(Rate=Rate)]
                EfficiencyList.append(Efficiency)

            MeanEfficiency = sum(EfficiencyList) / float(len(EfficiencyList))
            EfficienciesString = (EfficienciesString + "/{Eff:1.2f}".format(Eff=MeanEfficiency)).strip("/")

        self.ResultData['KeyValueDictPairs']['Efficiency'] = {
                'Value': EfficienciesString, 
                'Label': 'Efficiency %s'%RatesString,
                'Unit': '%',
            }

        ### Mean Noise ###
        self.ResultData['KeyValueDictPairs']['Noise'] = {
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['MeanNoise']['Value'], 
                'Label': 'Mean Noise',
                'Unit': 'e-',
            }

        self.ResultData['KeyList'] = ['Module', 'Grade', 'ManualGrade', 'ROCGrades','PixelDefects','BumpBondingDefects','NoisyPixels', 'HotPixelDefects', 'ROCsWithReadoutProblems', 'ROCsWithUniformityProblems', 'Efficiency','Noise']

        SpecialDefects = self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['SpecialDefects']
        if len(SpecialDefects) > 0:
            self.ResultData['KeyValueDictPairs']['SpecialDefects'] = {'Label': 'Defects', 'Value': SpecialDefects, 'Style': 'color:red; font-weight:bold;'}
            self.ResultData['KeyList'].append('SpecialDefects')

