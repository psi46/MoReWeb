import os

import ROOT

import AbstractClasses
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_TestResult'
        self.NameSingle = 'Fulltest'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = self.nTotalChips

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
                    'Order': 20,
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
        CurrentAtVoltage150V = -1
        RecalculatedVoltage = -1
        IVSlope = 0
        if self.ResultData['SubTestResults'].has_key('IVCurve'):
            CurrentAtVoltage150V = 0
            RecalculatedVoltage = 0
            #Check weather there is a recalculated current`
            if self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'].has_key(
                    'CurrentAtVoltage150V'):
                CurrentAtVoltage150V = float(
                    self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['CurrentAtVoltage150V'][
                        'Value'])
            if self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'].has_key(
                    'recalculatedCurrentAtVoltage150V'):
                RecalculatedVoltage = float(
                    self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'][
                        'recalculatedCurrentAtVoltage150V']['Value'])
            else:
                RecalculatedVoltage = CurrentAtVoltage150V
            if self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs'].has_key('Variation'):
                IVSlope = float(
                    self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['Variation']['Value'])
        initialCurrent = 0
        print 'fill row'
        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'Grade': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Grade']['Value'],
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

            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()
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


