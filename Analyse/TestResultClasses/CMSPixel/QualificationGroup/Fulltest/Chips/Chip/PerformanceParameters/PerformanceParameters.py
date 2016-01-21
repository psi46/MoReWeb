# -*- coding: utf-8 -*-
import AbstractClasses

try:
       set
except NameError:
       from sets import Set as set

def getDefectsListLength(defectsList):
    if type(defectsList) == list:
        return len(defectsList)
    else:
        return -1


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PerformanceParameters_TestResult'
        self.NameSingle='PerformanceParameters'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

        self.ResultData['KeyValueDictPairs'] = {
            'Total': {'Value':'-1', 'Label':'Total'},
            'nDeadPixel': {'Value':'-1', 'Label':' - Dead Pixels'},
            'nMaskDefect': {'Value':'-1', 'Label':' - Mask Defects'},
            'nDeadBumps': {'Value':'-1', 'Label':' - Dead Bumps'},
            'nDeadTrimbits': {'Value':'-1','Label':' - Dead Trimbits' },
            'nAddressProblems': {'Value':'-1', 'Label':' - Address Problems' },
            'nNoisy1Pixel': {'Value':'-1','Label':'>10 hits in alive map'},
            'nNoisy2Pixel': {'Value':'-1','Label':'Noisy Pixels'},
            'nThrDefect': {'Value':'-1','Label':'Trim Problems'},
            'nGainDefect': {'Value':'-1','Label':'PH Gain defects'},
            'nPedDefect': {'Value':'-1','Label':'PH Pedestal defects'},
            'nPar1Defect': {'Value':'-1','Label':'PH Parameter1 Defects'},
            'PixelDefectsGrade':{'Value': '0', 'Label': 'Pixel Defects Grade ROC'},
            'SCurveWidth_mu':{'Value': '-1','Label': 'SCurveWidth μ',},
            'SCurveWidth_sigma':{'Value': '-1','Label': 'SCurveWidth RMS',},
            'Noise':{'Value': '-1','Label': 'Mean Noise', 'Unit': 'e-',},
            'ThresholdTrimmed_mu':{'Value': '-1','Label': 'ThresholdTrimmed μ',},
            'ThresholdTrimmed_sigma':{'Value': '-1','Label': 'ThresholdTrimmed σ_fit',},
            'Threshold':{'Value': '-1','Label': 'Threshold','Unit': 'e-',},
            'ThresholdWidth':{'Value': '-1','Label': 'Threshold Width','Unit': 'e-',},
            'BumpBonding_mu':{'Value': '-1','Label': 'BumpBonding μ',},
            'BumpBonding_sigma':{'Value': '-1','Label': 'BumpBonding RMS',},
            'BumpBonding_threshold':{'Value': '-1','Label': 'BumpBonding Threshold',},
            'PHCalibrationGain_mu':{'Value': '-1','Label': 'PHCalibrationGain μ',},
            'PHCalibrationGain_sigma':{'Value': '-1','Label': 'PHCalibrationGain RMS',},
            'PHCalibrationPar1_mu':{'Value': '-1','Label': 'PHCalibrationParameter1 μ',},
            'PHCalibrationPar1_sigma':{'Value': '-1','Label': 'PHCalibrationParameter1 RMS',},
            'PHCalibrationPedestal_mu':{'Value': '-1','Label': 'PHCalibrationPedestal μ',},
            'PedestalSpread':{'Value': '-1','Label': 'PedestalSpread [e-]',},
            'PHCalibrationPedestal_sigma':{'Value': '-1','Label': 'PHCalibrationPedestal RMS',},
            'RelativeGainWidth':{'Value': '-1','Label': 'RelativeGainWidth',},
            'TrimBits_mu':{'Value': '-1','Label': 'TrimBits μ',},
            'TrimBits_sigma':{'Value': '-1','Label': 'TrimBits RMS',}
        }

    def PopulateResultData(self):

        SubtestGrading = self.ParentObject.ResultData['SubTestResults']['Grading']

        try:
            self.ResultData['KeyValueDictPairs'].update({
                'Total': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['TotalList'])),
                },
                'nDeadPixel': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['DeadPixelList'])),
                },
                'nMaskDefect': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['MaskDefectList'])),
                },
                'nDeadBumps': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['DeadBumpList'])),
                },
                'nDeadTrimbits': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['DeadTrimbitsList'])),
                },
                'nAddressProblems': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['AddressProblemList'])),
                },
                'nNoisy1Pixel': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['Noisy1PixelList'])),
                },
                'nNoisy2Pixel': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['NoiseDefectList'])),
                },
                'nThrDefect': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['ThrDefectList'])),
                },
                'nGainDefect': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['GainDefectList'])),
                },
                'nPedDefect': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['PedDefectList'])),
                },
                'nPar1Defect': {
                    'Value':'{0:1.0f}'.format(getDefectsListLength(SubtestGrading.ResultData['HiddenData']['Par1DefectList'])),
                },
            })
        except:
            pass

        try:
            self.ResultData['KeyValueDictPairs'].update({
                'PixelDefectsGrade':{
                    'Value': SubtestGrading.ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'],
                },
                'SCurveWidth_mu':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['KeyValueDictPairs']['mu']['Value'],
                },
                'SCurveWidth_sigma':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                },
                'Noise':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['KeyValueDictPairs']['mu']['Value'],
                },
                'ThresholdTrimmed_mu':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['mu']['Value'],
                },
                'ThresholdTrimmed_sigma':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                },
                'Threshold':{
                    'Value': '{0:1.0f}'.format(float(self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['mu']['Value'])
                            * self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']),
                },
                'ThresholdWidth':{
                    'Value': '{0:1.0f}'.format(float(self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['sigma']['Value'])
                            * self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']),
                },
                'BumpBonding_mu':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Mean']['Value'],
                },
                'BumpBonding_sigma':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['RMS']['Value'],
                },
                'BumpBonding_threshold':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Threshold']['Value'],
                },
                'PHCalibrationGain_mu':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['mu']['Value'],
                },
                'PHCalibrationGain_sigma':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                },
                'PHCalibrationPar1_mu':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationParameter1'].ResultData['KeyValueDictPairs']['Par1mu']['Value'],
                },
                'PHCalibrationPar1_sigma':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationParameter1'].ResultData['KeyValueDictPairs']['Par1sigma']['Value'],
                },
                'PHCalibrationPedestal_mu':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['mu']['Value'],
                },
                'PedestalSpread':{
                    'Value': '{0:1.0f}'.format(float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['sigma']['Value']) * self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']),
                },
                'PHCalibrationPedestal_sigma':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['PHCalibrationPedestal'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                },
                'RelativeGainWidth':{
                    'Value': '{0:1.3f}'.format(float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['sigma']['Value']) / float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['mu']['Value']) if float(self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['KeyValueDictPairs']['mu']['Value']) > 0 else 0),
                },
                'TrimBits_mu':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['KeyValueDictPairs']['mu']['Value'],
                },
                'TrimBits_sigma':{
                    'Value': self.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['KeyValueDictPairs']['sigma']['Value'],
                }
            })
        except:
            pass

        self.ResultData['KeyList'] = ['Noise', 'Threshold', 'ThresholdWidth', 'RelativeGainWidth', 'TrimBits_mu', 'TrimBits_sigma']
        # self.ResultData['KeyList'] = ['Total', 'nDeadPixel', 'nMaskDefect', 'nDeadBumps', 'nDeadTrimbits', 'nAddressProblems', 'empty',
        #                               'nNoisy1Pixel', 'nNoisy2Pixel', 'nThrDefect', 'nGainDefect', 'nPedDefect', 'nPar1Defect', 'PixelDefectsGrade',
        #                               'SCurveWidth_mu','SCurveWidth_sigma','ThresholdTrimmed_mu','ThresholdTrimmed_sigma','BumpBonding_mu',
        #                               'BumpBonding_sigma','BumpBonding_threshold','PHCalibrationGain_mu','PHCalibrationGain_sigma','PHCalibrationPar1_mu',
        #                               'PHCalibrationPar1_sigma','PHCalibrationPedestal_mu','PHCalibrationPedestal_sigma','TrimBits_mu','TrimBits_sigma']

