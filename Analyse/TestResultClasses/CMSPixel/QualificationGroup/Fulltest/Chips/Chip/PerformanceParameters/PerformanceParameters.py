# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

try:
       set
except NameError:
       from sets import Set as set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PerformanceParameters_TestResult'
        self.NameSingle='PerformanceParameters'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        

    def PopulateResultData(self):


        self.ResultData['KeyValueDictPairs'] = {
            'Total': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['TotalList'])),
                'Label':'Total'
            },
            'nDeadPixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadPixelList'])),
                'Label':' - Dead Pixels'
            },
            'nNoisy1Pixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Noisy1PixelList'])),
                'Label':'Noisy Pixels 1'
            },
            'nMaskDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['MaskDefectList'])),
                'Label':' - Mask Defects'
            },
            'nDeadBumps': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadBumpList'])),
                'Label':' - Dead Bumps'
            },
            'nDeadTrimbits': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadTrimbitsList'])),
                'Label':' - Dead Trimbits'
            },
            'nAddressProblems': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['AddressProblemList'])),
                'Label':' - Address Problems'
            },
            'nNoisy2Pixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NoisyPixelSCurveList'])),
                'Label':'Noisy Pixels 2'
            },
            'nThrDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['ThrDefectList'])),
                'Label':'Trim Problems'
            },
            'nGainDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['GainDefectList'])),
                'Label':'PH Gain defects'
            },
            'nPedDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['PedDefectList'])),
                'Label':'PH Pedestal defects'
            },
            'nPar1Defect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Par1DefectList'])),
                'Label':'PH Parameter1 Defects'
            },
            'PixelDefectsGrade':{
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'],
                'Label': 'Pixel Defects Grade ROC'
            },
            'SCurveWidth_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'SCurveWidth μ',
            },
            'SCurveWidth_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'SCurveWidth σ',
            },
            'ThresholdTrimmed_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'ThresholdTrimmed μ',
            },
            'ThresholdTrimmed_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'ThresholdTrimmed σ',
            },
            'BumpBonding_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Mean']['Value'],
                'Label': 'BumpBonding μ',
            },
            'BumpBonding_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['RMS']['Value'],
                'Label': 'BumpBonding σ',
            },
            'BumpBonding_threshold':{
                'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Threshold']['Value'],
                'Label': 'BumpBonding Threshold',
            },
            'PHCalibrationGain_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'PHCalibrationGain μ',
            },
            'PHCalibrationGain_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'PHCalibrationGain σ',
            },
            'PHCalibrationPar1_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationParameter1'].ResultData['KeyValueDictPairs']['Par1mu']['Value'],
                'Label': 'PHCalibrationParameter1 μ',
            },
            'PHCalibrationPar1_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationParameter1'].ResultData['KeyValueDictPairs']['Par1sigma']['Value'],
                'Label': 'PHCalibrationParameter1 σ',
            },
            'PHCalibrationPedestal_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'PHCalibrationPedestal μ',
            },
            'PHCalibrationPedestal_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'PHCalibrationPedestal σ',
            },
            'TrimBits_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'TrimBits μ',
            },
            'TrimBits_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'TrimBits σ',
            }
        }
        # self.ResultData['KeyList'] = ['Total', 'nDeadPixel', 'nMaskDefect', 'nDeadBumps', 'nDeadTrimbits', 'nAddressProblems', 'empty',
        #                               'nNoisy1Pixel', 'nNoisy2Pixel', 'nThrDefect', 'nGainDefect', 'nPedDefect', 'nPar1Defect', 'PixelDefectsGrade',
        #                               'SCurveWidth_mu','SCurveWidth_sigma','ThresholdTrimmed_mu','ThresholdTrimmed_sigma','BumpBonding_mu',
        #                               'BumpBonding_sigma','BumpBonding_threshold','PHCalibrationGain_mu','PHCalibrationGain_sigma','PHCalibrationPar1_mu',
        #                               'PHCalibrationPar1_sigma','PHCalibrationPedestal_mu','PHCalibrationPedestal_sigma','TrimBits_mu','TrimBits_sigma']

