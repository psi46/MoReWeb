import os
import sys
import ROOT

import AbstractClasses
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

from AbstractClasses.GeneralTestResult import GeneralTestResult
import subprocess

class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_TestResult'
        self.NameSingle = 'Fulltest'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = self.nTotalChips
        self.MergePyxarData()

        if self.Attributes['ModuleVersion'] == 1:
            if self.Attributes['ModuleType'] == 'a':
                self.Attributes['StartChip'] = 0
            elif self.Attributes['ModuleType'] == 'b':
                self.Attributes['StartChip'] = 7
            else:
                self.Attributes['StartChip'] = 0

        elif self.Attributes['ModuleVersion'] == 2:
            self.Attributes['StartChip'] = 0
        elif self.Attributes['ModuleVersion'] == 3:
            self.Attributes['NumberOfChips'] = 1
            self.Attributes['StartChip'] = 0
        ROCtype, nRocs, halfModule = self.ReadModuleVersion()
        self.Attributes['NumberOfChips'] = nRocs
        if halfModule:
            self.Attributes['StartChip'] = 8
        self.Attributes['isDigital'] = (ROCtype.find('dig') != -1)
        if self.verbose:
            print 'Analysing Fulltest with the following Attributes:'
            for name, value in self.Attributes.items():
                print "\t%25s:  %s" % (name, value)

        self.ResultData['SubTestResultDictList'] = [
            {
                'Key': 'DigitalCurrent',
                'DisplayOptions': {
                    'Order': 20,
                    'Width': 2
                }
            },
            {
                'Key': 'AnalogCurrent',
                'DisplayOptions': {
                    'Order': 21,
                    'Width': 2
                }
            },
            {
                'Key': 'Fitting',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Order': 99,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                },
            },
            {
                'Key': 'Temperature',
                'DisplayOptions': {
                    'GroupWithNext': False,
                    'Width': 2,
                    'Order': 25,
                },
            },
            {
                'Key': 'Chips',
                'DisplayOptions': {
                    'GroupWithNext': True,
                    'Order': 1,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },

            {
                'Key': 'BumpBondingMap',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 5,
                }
            },
            {
                'Key': 'VcalThreshold',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 3,
                }
            },
        ]
        # self.ResultData['SubTestResultDictList'].append({'Key': 'Temperature'})
        if not self.Attributes['isDigital']:
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'AddressLevelOverview',
                'DisplayOptions': {
                    'Order': 2,
                }
            })
        else:
            self.ResultData['SubTestResultDictList'].append(
                {
                    'Key': 'Dummy0',
                    'Module': 'Dummy',
                    'DisplayOptions': {
                        'Order': 2,
                    }
                },
            )

        if self.Attributes['IncludeIVCurve']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key': 'IVCurve',
                    'DisplayOptions': {
                        'Order': 8,
                        'Width': 3,
                    }
                },
            ]
        else:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key': 'Dummy1',
                    'Module': 'Dummy',
                    'DisplayOptions': {
                        'Order': 8,
                        'Width': 3,
                    }
                },
            ]

        self.ResultData['SubTestResultDictList'] += [
            {'Key': 'Noise', 'DisplayOptions': {'Order': 9, }},
            {'Key': 'VcalThresholdWidth', 'DisplayOptions': {'Order': 10, }},
            {'Key': 'RelativeGainWidth', 'DisplayOptions': {'Order': 11, }},
            {'Key': 'PedestalSpread', 'DisplayOptions': {'Order': 12, }},
        ]

        if self.Attributes['ModuleVersion'] == 1:
            self.ResultData['SubTestResultDictList'] += [
                {'Key': 'Parameter1', 'DisplayOptions': {'Order': 13, }}
            ]

        self.ResultData['SubTestResultDictList'] += [
        	     {
                'Key': 'Grading',
                'DisplayOptions': {
                    'Show': False,
                }
            },
            {
                'Key': 'Summary1',
                'DisplayOptions': {
                    'Order': 4,
                }
            },
            {
                'Key': 'Summary2',
                'DisplayOptions': {
                    'Order': 6,
                }
            },
            {
                'Key': 'Summary3',
                'DisplayOptions': {
                    'Order': 7,
                }
            },
            {
                'Key': 'SummaryROCs',
                'DisplayOptions': {
                    'Width': 4,
                }
            },
        ]

    def MergePyxarData(self):
        self.check_Test_Software()
        # raw_input(self.testSoftware)
        if self.testSoftware != 'pyxar':
            return
        print 'You are using pyxar. Trying to merge the subdirectories into one single root file.'
        subprocess.call(['../scripts/merge_pyxar_output.sh',self.RawTestSessionDataPath])

    def OpenFileHandle(self):
        self.check_Test_Software()
        fileHandlePath = self.RawTestSessionDataPath + '/commander_Fulltest.root'
        self.FileHandle = ROOT.TFile.Open(fileHandlePath)
        if not self.FileHandle:
            print 'problem to find %s' % fileHandlePath
            files = [f for f in os.listdir(self.RawTestSessionDataPath) if f.endswith('.root')]
            i = 0
            if len(files) > 1:
                print '\nPossible Candidates for ROOT files are:'
                for f in files:
                    print '\t[%3d]\t%s' % (i, f)
                    i += 1
                i = len(files)
                if self.HistoDict.has_option('RootFile', 'filename'):
                    print 'checking for backup rootfile name'
                    if self.HistoDict.has_option('RootFile', 'filename'):
                        if self.HistoDict.get('RootFile', 'filename') in files:
                            i = files.index(self.HistoDict.get('RootFile', 'filename'))
                            print 'rootfile exists: index ', i
                while i < 0 or i >= len(files):
                    try:
                        # TODO: How to continue when it happens in automatic processing...
                        rawInput = ''
                        i = 0
                        if self.verbose:
                            rawInput = raw_input(
                                'There are more than one possbile candidate for the ROOT file. Which file should be used? [0-%d]\t' % (
                                    len(files) - 1))
                            i = int(rawInput)
                        elif self.HistoDict.has_option('RootFile', 'filename'):
                            if self.HistoDict.get('RootFile', 'filename') in files:
                                i = files.index(self.HistoDict.get('RootFile', 'filename'))
                        else:
                            i = 0
                    except TypeError:
                        print '%s is not an integer, please enter a valid integer' % rawInput
                    except ValueError:
                        print '%s is not an integer, please enter a valid integer' % rawInput

                fileHandlePath = self.RawTestSessionDataPath + '/' + files[i]
                print "open '%s'" % fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            elif len(files) == 1:
                i = 0
                fileHandlePath = self.RawTestSessionDataPath + '/' + files[i]
                print "only one other ROOT file exists. Open '%s'" % fileHandlePath
                self.FileHandle = ROOT.TFile.Open(fileHandlePath)
            else:
                print 'There exist no ROOT file in "%s"' % self.RawTestSessionDataPath

    def PopulateResultData(self):
        self.FileHandle.Close()

    def CustomWriteToDatabase(self, ParentID):
        if self.verbose:
            print 'Write to DB: ',ParentID

        ####
        for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            # print ChipTestResultObject.ResultData['SubTestResults'].keys()
            PerformanceParametersTestResultObject =  ChipTestResultObject.ResultData['SubTestResults']['PerformanceParameters']
            PerformanceParameters = PerformanceParametersTestResultObject.ResultData['KeyValueDictPairs']
            if self.verbose:
                for i in PerformanceParameters:
                    print '\t',ChipNo, i,PerformanceParameters[i]['Value']
        ####
        CurrentAtVoltage150V = -1
        RecalculatedVoltage = -1
        IVSlope = 0
        if self.ResultData['SubTestResults'].has_key('IVCurve'):
            CurrentAtVoltage150V = 0
            # RecalculatedVoltage = 0
            #Check weather there is a recalculated current`
            if self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'].has_key(
                    'CurrentAtVoltage150V'):
                CurrentAtVoltage150V = float(
                    self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['CurrentAtVoltage150V'][
                        'Value'])
                CurrentAtVoltage150V *= self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['CurrentAtVoltage150V'].get('Factor',1)
            if self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'].has_key(
                    'recalculatedCurrentAtVoltage150V'):
                RecalculatedVoltage = float(
                    self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'][
                        'recalculatedCurrentAtVoltage150V']['Value'])
                RecalculatedVoltage *= self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V'].get('Factor',1)

            else:
                RecalculatedVoltage = CurrentAtVoltage150V
            if self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'].has_key('Variation'):
                IVSlope = float(
                    self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['Variation']['Value'])
        initialCurrent = 0

        try:
            grade = self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Grade']['Value']
        except KeyError:
            grade = 'None'
        print 'fill row'
        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'Grade': grade,
            'PixelDefects': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['DeadPixels'][
                'Value'],
            'ROCsMoreThanOnePercent':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['BadRocs']['Value'],
            'Noise': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoisyPixels'][
                'Value'],
            'Trimming': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['TrimProblems'][
                'Value'],
            'PHCalibration':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PHGainDefects']['Value'],
            'CurrentAtVoltage150V': CurrentAtVoltage150V,
            'RecalculatedVoltage': RecalculatedVoltage,
            'IVSlope': IVSlope,
            'Temperature': self.ResultData['SubTestResults']['Summary2'].ResultData['KeyValueDictPairs']['TempC'][
                'Value'],
            'RelativeModuleFinalResultsPath': os.path.relpath(self.TestResultEnvironmentObject.FinalModuleResultsPath,
                                                              self.TestResultEnvironmentObject.GlobalOverviewPath),
            'FulltestSubfolder': os.path.relpath(self.FinalResultsStoragePath,
                                                 self.TestResultEnvironmentObject.FinalModuleResultsPath),
            # needed for PixelDB
            'AbsModuleFulltestStoragePath': self.TestResultEnvironmentObject.FinalModuleResultsPath,
            'AbsFulltestSubfolder': self.FinalResultsStoragePath,
            'InputTarFile': os.environ.get('TARFILE', None),
            'MacroVersion': os.environ.get('MACROVERSION', None),
            #

            'initialCurrent': initialCurrent,
            'Comments': '',
            'nCycles': None,
            'CycleTempLow': None,
            'CycleTempHigh': None,

            #
            # added by Tommaso
            #
            'nMaskDefects':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['MaskDefects']['Value'],
            'nDeadPixels': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['DeadPixels'][
                'Value'],
            'nBumpDefects': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['DeadBumps'][
                'Value'],
            'nTrimDefects':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['TrimProblems']['Value'],
            'nNoisyPixels':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'],
            'nGainDefPixels':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PHGainDefects']['Value'],
            'nPedDefPixels':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PHPedestalDefects'][
                    'Value'],
            'nPar1DefPixels':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PHPar1Defects']['Value'],

            'TestCenter': self.Attributes['TestCenter'],
            'Hostname': self.Attributes['Hostname'],
            'Operator': self.Attributes['Operator'],
            #
            # added by Felix for the new Overview Table
            #
            # for A/B/C sub gradings
            'PixelDefectsNGradeA':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PixelDefectsGradeAROCs'][
                    'Value'],
            'PixelDefectsNGradeB':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PixelDefectsGradeBROCs'][
                    'Value'],
            'PixelDefectsNGradeC':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PixelDefectsGradeCROCs'][
                    'Value'],

            'NoiseNGradeA':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeAROCs'][
                    'Value'],
            'NoiseNGradeB':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeBROCs'][
                    'Value'],
            'NoiseNGradeC':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeCROCs'][
                    'Value'],

            'VcalWidthNGradeA': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'VcalThresholdWidthGradeAROCs']['Value'],
            'VcalWidthNGradeB': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'VcalThresholdWidthGradeBROCs']['Value'],
            'VcalWidthNGradeC': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'VcalThresholdWidthGradeCROCs']['Value'],

            'GainNGradeA': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'RelativeGainWidthGradeAROCs']['Value'],
            'GainNGradeB': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'RelativeGainWidthGradeBROCs']['Value'],
            'GainNGradeC': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'RelativeGainWidthGradeCROCs']['Value'],

            'PedSpreadNGradeA': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'PedestalSpreadGradeAROCs']['Value'],
            'PedSpreadNGradeB': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'PedestalSpreadGradeBROCs']['Value'],
            'PedSpreadNGradeC': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs'][
                'PedestalSpreadGradeCROCs']['Value'],

            'Par1NGradeA':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Parameter1GradeAROCs'][
                    'Value'],
            'Par1NGradeB':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Parameter1GradeBROCs'][
                    'Value'],
            'Par1NGradeC':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Parameter1GradeCROCs'][
                    'Value'],
        }
        print 'fill row end'
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            from PixelDB import *
            # modified by Tommaso
            #
            # try and speak directly with PixelDB
            #

#            fake = int(os.environ.get('FAKE',1))

#            insertedID=7
            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()
            
            if (0 == 0):
                OPERATOR = os.environ['PIXEL_OPERATOR']
                CENTER = os.environ['PIXEL_CENTER']
                s = Session(CENTER, OPERATOR)
                pdb.insertSession(s)
                print "--------------------"
                print "INSERTING INTO DB", self.TestResultEnvironmentObject.FinalModuleResultsPath, s.SESSION_ID, Row
                print "--------------------"
                pp = pdb.insertTestFullModuleDirPlusMapv96Plus(s.SESSION_ID, Row)
                
                if pp is None:
                    print "INSERTION FAILED!"
                    sys.exit(31)

                insertedID=pp.TEST_ID

#
# also insert dac parameters
#
#
#                you can access it via self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']['Chip'+int(ChipNo)].ResultData['SubTestResults']['DacParameterOverview'].ResultData['SubTestResults']['DacParameters'+int(TrimValue)].ResultData['KeyValueDictPairs']
            #
                    
            if (0==0):
                for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                    ChipTestResultObject = self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                    ChipNo = ChipTestResultObject.Attributes['ChipNo']
                    DacParameterOverviewTestResultObject =  ChipTestResultObject.ResultData['SubTestResults']['DacParameterOverview']
                    
                    for j in DacParameterOverviewTestResultObject.ResultData['SubTestResults']:
                        DacParameterTestResultObject = DacParameterOverviewTestResultObject.ResultData['SubTestResults'][j]
                        DacParameters = DacParameterTestResultObject.ResultData['KeyValueDictPairs']

#CHIP 5 {'VIon': {'Value': '130', 'Label': 'VIon'}, 'VwllSh': {'Value': '35', 'Label': 'VwllSh'}, 'Vcal': {'Value': '199', 'Label': 'Vcal'}, 'VhldDel': {'Value': '160', 'Label': 'VhldDel'}, 'Vtrim': {'Value': '7', 'Label': 'Vtrim'}, 'VthrComp': {'Value': '92', 'Label': 'VthrComp'}, 'VrgPr': {'Value': '0', 'Label': 'VrgPr'}, 'Vleak_comp': {'Value': '0', 'Label': 'Vleak_comp'}, 'Vbias_sf': {'Value': '10', 'Label': 'Vbias_sf'}, 'Vana': {'Value': '128', 'Label': 'Vana'}, 'Vdig': {'Value': '6', 'Label': 'Vdig'}, 'RangeTemp': {'Value': '0', 'Label': 'RangeTemp'}, 'VIbias_PH': {'Value': '220', 'Label': 'VIbias_PH'}, 'VIbias_roc': {'Value': '220', 'Label': 'VIbias_roc'}, 'TrimBits_mu': {'Value': '15.00', 'Label': 'TrimBit Mean'}, 'VIColOr': {'Value': '99', 'Label': 'VIColOr'}, 'VOffsetR0': {'Value': '120', 'Label': 'VOffsetR0'}, 'CalDel': {'Value': '85', 'Label': 'CalDel'}, 'TrimValue': {'Value': '-1', 'Label': 'TrimValue'}, 'VrgSh': {'Value': '0', 'Label': 'VrgSh'}, 'VSumCol': {'Value': '0', 'Label': 'VSumCol'}, 'TrimBits_sigma': {'Value': '0.00', 'Label': 'TrimBit sigma'}, 'VwllPr': {'Value': '35', 'Label': 'VwllPr'}, 'CtrlReg': {'Value': '0', 'Label': 'CtrlReg'}, 'Vnpix': {'Value': '0', 'Label': 'Vnpix'}, 'VIbiasOp': {'Value': '50', 'Label': 'VIbiasOp'}, 'Vcomp': {'Value': '10', 'Label': 'Vcomp'}, 'VIBias_Bus': {'Value': '30', 'Label': 'VIBias_Bus'}, 'Ibias_DAC': {'Value': '36', 'Label': 'Ibias_DAC'}, 'Vsf': {'Value': '150', 'Label': 'Vsf'}, 'VoffsetOp': {'Value': '92', 'Label': 'VoffsetOp'}, 'WBC': {'Value': '100', 'Label': 'WBC'}}
#                        print"PIPPONE",i,j
                        print "INPUT", DacParameters

                        dacparam = Test_DacParameters(
                            ROC_POS= ChipNo,
                            TRIM_VALUE= DacParameters['TrimValue']['Value'], #DACPARAMETERS = j,
                            FULLMODULEANALYSISTEST_ID = insertedID,   ## NOT SURE!!!!! this seems to be an analysis!!!!
                            VDIG = DacParameters['vdig']['Value'],
                            VANA = DacParameters['vana']['Value'], 
                            VSH = DacParameters['vsh']['Value'],
                            VCOMP = DacParameters['vcomp']['Value'],
                            VCAL = DacParameters['vcal']['Value'],
                            VWLLPR = DacParameters['vwllpr']['Value'],
                            VWLLSH = DacParameters['vwllsh']['Value'],
                            VTRIM = DacParameters['vtrim']['Value'],
                            VTHRCOMP = DacParameters['vthrcomp']['Value'],
                            VHLDDEL = DacParameters['vhlddel']['Value'],
                            VIBIAS_BUS = DacParameters['vibias_bus']['Value'],
                            PHOFFSET = DacParameters['phoffset']['Value'],
                            VCOMP_ADC = DacParameters['vcomp_adc']['Value'],
                            PHSCALE = DacParameters['phscale']['Value'],
                            #
                            VICOLOR = DacParameters['vicolor']['Value'],
                            CALDEL = DacParameters['caldel']['Value'],
                            CTRLREG = DacParameters['ctrlreg']['Value'],
                            WBC = DacParameters['wbc']['Value'])
                        pdb.insertTestDac(dacparam)
                        print "DAC TEST INSERTED FOR", ChipNo, insertedID, j

            if (0 ==0):
                for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
                    ChipTestResultObject = self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                    ChipNo = ChipTestResultObject.Attributes['ChipNo']
#                    print "PIPPO!!!!!",ChipNo
                # print ChipTestResultObject.ResultData['SubTestResults'].keys()
                    PerformanceParametersTestResultObject =  ChipTestResultObject.ResultData['SubTestResults']['PerformanceParameters']
                    PerformanceParameters = PerformanceParametersTestResultObject.ResultData['KeyValueDictPairs']
#                    print "PAYLOAD ", PerformanceParameters
#PAYLOAD  {'nDeadTrimbits': {'Value': '0', 'Label': ' - Dead Trimbits'}, 'PHCalibrationPedestal_mu': {'Value': '96.65', 'Label': 'PHCalibrationPedestal \xce\xbc'}, 'nDeadPixel': {'Value': '0', 'Label': ' - Dead Pixels'}, 'PHCalibrationPar1_sigma': {'Value': '0.06', 'Label': 'PHCalibrationParameter1 \xcf\x83'}, 'BumpBonding_mu': {'Value': -16.800000000000001, 'Label': 'BumpBonding \xce\xbc'}, 'BumpBonding_threshold': {'Value': -6.1200000000000001, 'Label': 'BumpBonding Threshold'}, 'nMaskDefect': {'Value': '0', 'Label': ' - Mask Defects'}, 'nDeadBumps': {'Value': '0', 'Label': ' - Dead Bumps'}, 'PHCalibrationGain_mu': {'Value': '0.58', 'Label': 'PHCalibrationGain \xce\xbc'}, 'nNoisy1Pixel': {'Value': '0', 'Label': 'Noisy Pixels 1'}, 'nPedDefect': {'Value': '0', 'Label': 'PH Pedestal defects'}, 'BumpBonding_sigma': {'Value': 2.1400000000000001, 'Label': 'BumpBonding \xcf\x83'}, 'ThresholdTrimmed_mu': {'Value': '60.10', 'Label': 'ThresholdTrimmed \xce\xbc'}, 'PHCalibrationGain_sigma': {'Value': '0.02', 'Label': 'PHCalibrationGain \xcf\x83'}, 'PHCalibrationPedestal_sigma': {'Value': '33.73', 'Label': 'PHCalibrationPedestal \xcf\x83'}, 'nPar1Defect': {'Value': '0', 'Label': 'PH Parameter1 Defects'}, 'TrimBits_sigma': {'Value': '1.77', 'Label': 'TrimBits \xcf\x83'}, 'SCurveWidth_mu': {'Value': '121.67', 'Label': 'SCurveWidth \xce\xbc'}, 'TrimBits_mu': {'Value': '9.36', 'Label': 'TrimBits \xce\xbc'}, 'PixelDefectsGrade': {'Value': '1', 'Label': 'Pixel Defects Grade ROC'}, 'ThresholdTrimmed_sigma': {'Value': '1.37', 'Label': 'ThresholdTrimmed \xcf\x83'}, 'PHCalibrationPar1_mu': {'Value': '0.81', 'Label': 'PHCalibrationParameter1 \xce\xbc'}, 'nAddressProblems': {'Value': '0', 'Label': ' - Address Problems'}, 'SCurveWidth_sigma': {'Value': '11.86', 'Label': 'SCurveWidth \xcf\x83'}, 'nNoisy2Pixel': {'Value': '0', 'Label': 'Noisy Pixels 2'}, 'Total': {'Value': '0', 'Label': 'Total'}, 'nThrDefect': {'Value': '0', 'Label': 'Trim Problems'}, 'nGainDefect': {'Value': '0', 'Label': 'PH Gain defects'}}
                    
                    test = Test_PerformanceParameters(
                        FULLMODULEANALYSISTEST_ID = insertedID, #### beware this is an analysis!
                        ROC_POS = ChipNo,
                        Total = PerformanceParameters['Total']['Value'], 
                        nDeadPixel  = PerformanceParameters['nDeadPixel']['Value'],
                        nMaskDefect  = PerformanceParameters['nMaskDefect']['Value'],
                        nDeadBumps  = PerformanceParameters['nDeadBumps']['Value'],
                        nDeadTrimbits  = PerformanceParameters['nDeadTrimbits']['Value'],
                        nAddressProblems  = PerformanceParameters['nAddressProblems']['Value'],
                        nNoisy1Pixel  = PerformanceParameters['nNoisy1Pixel']['Value'],
                        nNoisy2Pixel  = PerformanceParameters['nNoisy2Pixel']['Value'],
                        nThrDefect  = PerformanceParameters['nThrDefect']['Value'],
                        nGainDefect  = PerformanceParameters['nGainDefect']['Value'],
                        nPedDefect  = PerformanceParameters['nPedDefect']['Value'],
                        nPar1Defect  = PerformanceParameters['nPar1Defect']['Value'],
                        PixelDefectsGrade  = PerformanceParameters['PixelDefectsGrade']['Value'],
                        SCurveWidth_mu = PerformanceParameters['SCurveWidth_mu']['Value'],  
                        SCurveWidth_sigma= PerformanceParameters['SCurveWidth_sigma']['Value'],
                        ThresholdTrimmed_mu= PerformanceParameters['ThresholdTrimmed_mu']['Value'],
                        ThresholdTrimmed_sigma= PerformanceParameters['ThresholdTrimmed_sigma']['Value'],
                        BumpBonding_mu= PerformanceParameters['BumpBonding_mu']['Value'],
                        BumpBonding_sigma= PerformanceParameters['BumpBonding_sigma']['Value'],
                        BumpBonding_threshold= PerformanceParameters['BumpBonding_threshold']['Value'],
                        PHCalibrationGain_mu= PerformanceParameters['PHCalibrationGain_mu']['Value'],
                        PHCalibrationGain_sigma= PerformanceParameters['PHCalibrationGain_sigma']['Value'],
                        PHCalibrationPar1_mu= PerformanceParameters['PHCalibrationPar1_mu']['Value'],
                        PHCalibrationPar1_sigma= PerformanceParameters['PHCalibrationPar1_sigma']['Value'],
                        PHCalibrationPedestal_mu= PerformanceParameters['PHCalibrationPedestal_mu']['Value'],
                        PHCalibrationPedestal_sigma= PerformanceParameters['PHCalibrationPedestal_sigma']['Value'],
                        TrimBits_mu= PerformanceParameters['TrimBits_mu']['Value'],
                        TrimBits_sigma= PerformanceParameters['TrimBits_sigma']['Value'])
                    pdb.insertTestPerformance(test)
                    print "PERFORMANCE TEST INSERTED FOR", ChipNo, insertedID
#                    for i in PerformanceParameters:
#                        print '\t',ChipNo, i,PerformanceParameters[i]['Value']
#
# insert performance parameters
#                    

        else:
            with self.TestResultEnvironmentObject.LocalDBConnection:
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    'DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType=:TestType AND QualificationType=:QualificationType AND TestDate <= :TestDate',
                    Row)
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    '''INSERT INTO ModuleTestResults
                    (
                        ModuleID,
                        TestDate,
                        TestType,
                        QualificationType,
                        Grade,
                        PixelDefects,
                        ROCsMoreThanOnePercent,
                        Noise,
                        Trimming,
                        PHCalibration,
                        CurrentAtVoltage150V,
                        RecalculatedVoltage,
                        IVSlope,
                        Temperature,
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder,
                        initialCurrent,
                        Comments,
                        nCycles,
                        CycleTempLow,
                        CycleTempHigh
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :PixelDefects,
                        :ROCsMoreThanOnePercent,
                        :Noise,
                        :Trimming,
                        :PHCalibration,
                        :CurrentAtVoltage150V,
                        :RecalculatedVoltage,
                        :IVSlope,
                        :Temperature,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder,
                        :initialCurrent,
                        :Comments,
                        :nCycles,
                        :CycleTempLow,
                        :CycleTempHigh
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid


