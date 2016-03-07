# -*- coding: utf-8 -*-
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'DoubleColumnGrading'
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {}
        self.ResultData['KeyValueDictPairs']['NBadDoubleColumns'] = {
            'Label': '# Bad Double Columns',
            'Value': '-1'
        }
        self.ResultData['KeyValueDictPairs']['BadDoubleColumns'] = {
            'Label': 'Bad Double Columns',
            'Value': set()
        }

        self.ResultData['HiddenData']['InefficientPixelList'] = set()
        self.ResultData['HiddenData']['HighRateInefficientPixelList'] = set()
        self.ResultData['HiddenData']['NoisyPixelList'] = set()
        self.ResultData['HiddenData']['BumpDefectList'] = set()
        self.ResultData['HiddenData']['DefectsGradingComplete'] = False

    def PopulateResultData(self):

        ChipNo = self.ParentObject.Attributes['ChipNo']

        # get defects lists for individual defects
        BumpBondingTestRate = max(self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRData'])
        BumpBondingTestResults = self.ParentObject.ResultData['SubTestResults']['BumpBondingDefects_{Rate}'.format(Rate=BumpBondingTestRate)]
        self.ResultData['HiddenData']['BumpDefectList'] = BumpBondingTestResults.ResultData['HiddenData']['ListOfDefectivePixels']['Value']

        NoiseTestRate = max(self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRSCurves'])
        NoiseTestResults = self.ParentObject.ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=NoiseTestRate)]
        self.ResultData['HiddenData']['NoisyPixelList'] = NoiseTestResults.ResultData['HiddenData']['ListOfNoisyPixels']['Value']

        EfficiencyTestResult = self.ParentObject.ResultData['SubTestResults']['PixelEfficiency']
        self.ResultData['HiddenData']['HighRateInefficientPixelList'] = EfficiencyTestResult.ResultData['KeyValueDictPairs']['HighRateInefficientPixels']['Value']
        self.ResultData['HiddenData']['InefficientPixelList'] = EfficiencyTestResult.ResultData['KeyValueDictPairs']['InefficientPixels']['Value']

        # compute union of all sets of bad pixels
        self.ResultData['HiddenData']['DefectsGradingComplete'] = True
        self.ResultData['HiddenData']['TotalList'] = set([])
        for IndividualDefectsList in [
            self.ResultData['HiddenData']['HighRateInefficientPixelList'],
            self.ResultData['HiddenData']['InefficientPixelList'],
            self.ResultData['HiddenData']['NoisyPixelList'],
            self.ResultData['HiddenData']['BumpDefectList'],
        ]:
            if IndividualDefectsList is not None:
                self.ResultData['HiddenData']['TotalList'] = self.ResultData['HiddenData']['TotalList'] | IndividualDefectsList
            else:
                self.ResultData['HiddenData']['DefectsGradingComplete'] = False


        MaximumNumberAllowedBadPixels = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_bad_pixels_per_double_column']

        # check for number of defects per double column
        for DoubleColumn in range(0, 26):

            # inefficienct pixels: >1% per double column => C
            NEfficiencyDefectsPerDoubleColumn = len([x for x in self.ResultData['HiddenData']['HighRateInefficientPixelList'] if x[0] == ChipNo and int(x[1]/2) == DoubleColumn])
            if NEfficiencyDefectsPerDoubleColumn > MaximumNumberAllowedBadPixels:
                self.ResultData['KeyValueDictPairs']['BadDoubleColumns']['Value'].add((ChipNo, DoubleColumn))

        self.ResultData['KeyValueDictPairs']['NBadDoubleColumns']['Value'] = len(self.ResultData['KeyValueDictPairs']['BadDoubleColumns']['Value'])
