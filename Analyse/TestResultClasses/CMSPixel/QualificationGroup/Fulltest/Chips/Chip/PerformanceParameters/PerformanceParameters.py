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
            'nNoisy1Pixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Noisy1PixelList'])),
                'Label':'>10 hits in alive map'
            },
            'nNoisy2Pixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NoiseDefectList'])),
                'Label':'Noisy Pixels'
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
                'Label': 'SCurveWidth RMS',
            },
            'Noise':{
                'Value': self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'Mean Noise',
                'Unit': 'e-',
            },
            'ThresholdTrimmed_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'ThresholdTrimmed μ',
            },
            'ThresholdTrimmed_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'ThresholdTrimmed σ_fit',
            },
            'Threshold':{
                'Value': '{0:1.0f}'.format(float(self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['mu']['Value'])
                        * self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']),
                'Label': 'Threshold',
                'Unit': 'e-',
            },
            'ThresholdWidth':{
                'Value': '{0:1.0f}'.format(float(self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['sigma']['Value'])
                        * self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']),
                'Label': 'Threshold Width',
                'Unit': 'e-',
            },
            'BumpBonding_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Mean']['Value'],
                'Label': 'BumpBonding μ',
            },
            'BumpBonding_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['RMS']['Value'],
                'Label': 'BumpBonding RMS',
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
                'Label': 'PHCalibrationGain RMS',
            },
            'PHCalibrationPar1_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationParameter1'].ResultData['KeyValueDictPairs']['Par1mu']['Value'],
                'Label': 'PHCalibrationParameter1 μ',
            },
            'PHCalibrationPar1_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationParameter1'].ResultData['KeyValueDictPairs']['Par1sigma']['Value'],
                'Label': 'PHCalibrationParameter1 RMS',
            },
            'PHCalibrationPedestal_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'PHCalibrationPedestal μ',
            },            
            'PedestalSpread':{
                'Value': '{0:1.0f}'.format(float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['sigma']['Value']) * self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']),
                'Label': 'PedestalSpread [e-]',
            },
            'PHCalibrationPedestal_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'PHCalibrationPedestal RMS',
            },
            'RelativeGainWidth':{
                'Value': '{0:1.3f}'.format(float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['sigma']['Value']) / float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['mu']['Value']) if float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['mu']['Value']) > 0 else 0),
                'Label': 'RelativeGainWidth',
            },
            'TrimBits_mu':{
                'Value': self.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['KeyValueDictPairs']['mu']['Value'],
                'Label': 'TrimBits μ',
            },
            'TrimBits_sigma':{
                'Value': self.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                'Label': 'TrimBits RMS',
            }
        }
        self.ResultData['KeyList'] = ['Noise', 'Threshold', 'ThresholdWidth', 'RelativeGainWidth', 'TrimBits_mu', 'TrimBits_sigma']
        # self.ResultData['KeyList'] = ['Total', 'nDeadPixel', 'nMaskDefect', 'nDeadBumps', 'nDeadTrimbits', 'nAddressProblems', 'empty',
        #                               'nNoisy1Pixel', 'nNoisy2Pixel', 'nThrDefect', 'nGainDefect', 'nPedDefect', 'nPar1Defect', 'PixelDefectsGrade',
        #                               'SCurveWidth_mu','SCurveWidth_sigma','ThresholdTrimmed_mu','ThresholdTrimmed_sigma','BumpBonding_mu',
        #                               'BumpBonding_sigma','BumpBonding_threshold','PHCalibrationGain_mu','PHCalibrationGain_sigma','PHCalibrationPar1_mu',
        #                               'PHCalibrationPar1_sigma','PHCalibrationPedestal_mu','PHCalibrationPedestal_sigma','TrimBits_mu','TrimBits_sigma']

