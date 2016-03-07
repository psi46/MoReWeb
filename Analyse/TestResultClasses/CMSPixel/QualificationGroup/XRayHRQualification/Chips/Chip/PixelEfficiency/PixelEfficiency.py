# -*- coding: utf-8 -*-
import AbstractClasses

# scans the calibrate signal maps for all rates in the efficiency test and count inefficient single pixels

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'PixelEfficiency'
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {}
        self.ResultData['KeyValueDictPairs']['NInefficientPixels'] = {
            'Label': '# Inefficient Pixels',
            'Value': '-1'
        }
        self.ResultData['KeyValueDictPairs']['InefficientPixels'] = {
            'Label': 'Inefficient Pixels',
            'Value': ''
        }
        self.ResultData['KeyValueDictPairs']['HighRateInefficientPixels'] = {
            'Label': 'HR Inefficient Pixels',
            'Value': ''
        }
        self.ResultData['KeyList'] = ['InefficientPixels', 'NInefficientPixels']
        self.InefficienctPixelList = set()
        self.HighRateInefficientPixelsList = set()


    def PopulateResultData(self):
        self.Canvas.Clear()

        ChipNo = self.ParentObject.Attributes['ChipNo']
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']

        try:
            histoAlive = self.ParentObject.ResultData['SubTestResults']['AliveMap'].ResultData['Plot']['ROOTObject']
        except:
            histoAlive = None

        # scan all rates of the efficiency test
        for Rate in Rates['HREfficiency']:

            # and all double columns
            for DoubleColumn in range(0, 26):

                Ntrig = self.ParentObject.ParentObject.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)]
                EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']

                PixelEfficiencyMean = EfficiencyMapROOTObject.GetMean()
                PixelEfficiencyRMS = EfficiencyMapROOTObject.GetRMS()
                PixelEfficiencyThreshold = min(self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_bad_pixels_cut_max'], max(self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_bad_pixels_cut_min'], PixelEfficiencyMean - self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_bad_pixels_cut_sigma'] * PixelEfficiencyRMS))

                for PixNo in range(0, 160):
                    col = DoubleColumn * 2 + (1 if PixNo > 79 else 0)
                    row = PixNo % 80
                    PixelNHits = EfficiencyMapROOTObject.GetBinContent(col + 1, row + 1)
                    PixelEfficiency = PixelNHits/Ntrig

                    if PixelEfficiency < PixelEfficiencyThreshold:
                        # inefficient pixels, including dead pixels. Used for pixel-based grading only
                        self.InefficienctPixelList.add((ChipNo, col, row))

                        # inefficient pixels, excluding dead pixels, Used for double column defects detection
                        if histoAlive is None or histoAlive.GetBinContent(col + 1, row + 1) > 0:
                            self.HighRateInefficientPixelsList.add((ChipNo, col, row))


        self.ResultData['KeyValueDictPairs']['InefficientPixels']['Value'] = self.InefficienctPixelList
        self.ResultData['KeyValueDictPairs']['HighRateInefficientPixels']['Value'] = self.HighRateInefficientPixelsList
        self.ResultData['KeyValueDictPairs']['NInefficientPixels']['Value'] = len(self.InefficienctPixelList)

