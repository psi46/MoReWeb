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
            },
            'PixelDefects': {
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefects']['Value'],
                'Label': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefects']['Label']
            }
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
        RatesString = ''
        NoiseString = ''
        for Rate in self.ParentObject.Attributes['Rates']['HRSCurves']:
            RatesString = (RatesString + "/{Rate}".format(Rate=Rate)).strip("/")

            NoiseList = []
            for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                Noise = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Noise_{Rate}'.format(Rate=Rate)]
                NoiseList.append(Noise)

            MeanNoise = sum(NoiseList) / float(len(NoiseList))
            NoiseString = (NoiseString + "/{Noise:1.0f}".format(Noise=MeanNoise)).strip("/")

            break #allow only one noise rate for now

        self.ResultData['KeyValueDictPairs']['Noise'] = {
                'Value': NoiseString, 
                'Label': 'Noise %s'%RatesString,
                'Unit': 'e-',
            }

        ### Noisy Pixels ###
        RatesString = ''
        NoiseString = ''
        for Rate in self.ParentObject.Attributes['Rates']['HRSCurves']:
            RatesString = (RatesString + "/{Rate}".format(Rate=Rate)).strip("/")

            NoiseList = []
            for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                Noise = ChipTestResultObject.ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=Rate)].ResultData['HiddenData']['NumberOfNoisyPixels']
                NoiseList.append(Noise)

            TotalNoisyPixels = sum(NoiseList)
            NoiseString = (NoiseString + "/{Noise:1.0f}".format(Noise=TotalNoisyPixels)).strip("/")

            break #allow only one noise rate for now

        self.ResultData['KeyValueDictPairs']['NoisyPixels'] = {
                'Value': NoiseString, 
                'Label': 'Noisy Pixels %s'%RatesString,
                'Unit': '',
            }

        self.ResultData['KeyList'] = ['Module','Grade', 'ROCGrades','PixelDefects','Efficiency','Noise','NoisyPixels']


