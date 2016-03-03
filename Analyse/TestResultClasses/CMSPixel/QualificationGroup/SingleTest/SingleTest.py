import os
import sys
import ROOT
import warnings

import AbstractClasses
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

from AbstractClasses.GeneralTestResult import GeneralTestResult
import subprocess

class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'SingleTest'
        self.Name = 'CMSPixel_QualificationGroup_%s_TestResult'%self.NameSingle 
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ReadModuleVersion()
        self.Attributes['NumberOfChips'] = self.nRocs
        self.Attributes['StartChip'] = 0
        self.Attributes['ModuleVersion'] = 1
        self.Attributes['isDigital'] = 1

        self.AddCommentsToKeyValueDictPairs = True

        TestNameDictionary = {
            'PixelAlive': {
                'ChipTests': ['TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap'],
                'Tests': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.PixelMap',
                        'Width': 4,
                    }
                ],
            },
            'BumpBonding': {
                'ChipTests': [
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBonding',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingProblems',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.BumpBondingMap',
                ],
                'Tests': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.BumpBondingProblems',
                        'Width': 4,
                        'InitialAttributes': {
                                'StorageKey': 'BBThrMap',
                            },
                    },
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.BumpBondingMap',
                        'Width': 4,
                        'InitialAttributes': {
                                'StorageKey': 'BBDefectsMap',
                        },
                    }
                ],
            },
            'Scurves': {
                'Fitting': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Fitting',
                    }],
                'ChipTests': [
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.SCurveWidths',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.VcalThresholdUntrimmed',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ThresholdDistribution',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.NoiseMap',
                ],
                'Tests': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.VcalThreshold',
                        'Width': 4,
                        'InitialAttributes': {
                                'StorageKey': 'VcalThreshold',
                        },
                    },
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Noise',
                        'Width': 1,
                        'InitialAttributes': {
                                'StorageKey': 'Noise',
                            },
                    },
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.NoiseMap',
                        'Width': 4,
                        'InitialAttributes': {
                                'StorageKey': 'NoiseMap',
                        },
                    },
                ],
            },
            'Trim': {
                'ChipTests': [
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.TrimBitTest',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.TrimBits',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.TrimBitMap',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.TrimBitProblems',
                ],
                'Tests': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.TrimBitMap',
                        'Width': 4,
                        'InitialAttributes': {
                                'StorageKey': 'TrimBitMap',
                        },
                    }
                ],
            },
            'PhOptimization': {
                'ChipTests': [
                    {
                        'Key': 'PHMapMax',
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PHMap',
                        'Width': 4,
                        'InitialAttributes': {
                            'StorageKey': 'PhMapMax',
                            'Map': 'MaxPHMap',
                        },
                    },
                    {
                        'Key': 'PHMapMin',
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PHMap',
                        'Width': 4,
                        'InitialAttributes': {
                            'StorageKey': 'PhMapMin',
                            'Map': 'MinPHMap',
                        },
                    },
                ],
                'Tests':
                    [],
            },
            'GainPedestal': {
                'Fitting': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Fitting',
                    }],
                'ChipTests': [
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.' + x for x in [
                        'PHCalibrationTan', 'PHCalibrationGain', 'PHCalibrationParameter1', 'PHCalibrationPedestal',
                        'PHCalibrationGainMap'
                        ]
                    ],
                'Tests': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.RelativeGainWidth',
                        'Width': 1,
                        'InitialAttributes': {
                                'StorageKey': 'RelativeGainWidth',
                        },
                    },
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.PedestalSpread',
                        'Width': 1,
                        'InitialAttributes': {
                                'StorageKey': 'PedestalSpread',
                            },
                    },
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Parameter1',
                        'Width': 1,
                        'InitialAttributes': {
                                'StorageKey': 'Parameter1',
                        },
                    },
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.GainMap',
                        'Width': 4,
                        'InitialAttributes': {
                                'StorageKey': 'GainMap',
                        },
                    },
                ],
            },
            'Hitmap': {
                'ChipTests': [
                    'TestResultClasses.CMSPixel.QualificationGroup.XRayHRQualification.Chips.Chip.HitMap',
                    ],
                'Tests': [
                    {
                        'Module': 'TestResultClasses.CMSPixel.QualificationGroup.XRayHRQualification.HitOverview',
                        'Width': 4,
                        'InitialAttributes': {
                                'StorageKey': 'HitOverview',
                        },
                    },
                ],
            },
            'ReadbackCal': {
                'ChipTests': [
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCal',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCalIana',
                    'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCalVdig',
                ],
                'Tests':
                    [
                        {
                            'Module': 'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.ReadbackParameter',
                            'InitialAttributes': {
                                'Parameter': '%s'%Parameter,
                                'StorageKey': 'ReadbackParameter_%s'%Parameter,
                            },
                        } for Parameter in ['par0vd', 'par1vd','par0va','par1va','par0rbia','par1rbia','par0tbia','par1tbia','par2tbia']
                    ],
            },

        }

        TestName = self.Attributes['Test']
        print "checking test '%s'"%TestName
        if TestName in TestNameDictionary:

            if 'Fitting' in TestNameDictionary[TestName]:
                for Test in TestNameDictionary[TestName]['Fitting']:
                    print "do fitting: ",Test['Module']
                    InitialAttributes = {
                            'ModuleVersion': self.Attributes['ModuleVersion'],
                            'NumberOfChips': self.Attributes['NumberOfChips'],
                            'StorageKey': Test['Module'],
                    }

                    if 'InitialAttributes' in Test:
                        InitialAttributes.update(Test['InitialAttributes'])

                    self.ResultData['SubTestResultDictList'].append(
                        {
                            'Key': Test['Module'],
                            'DisplayOptions': {
                                'Show': False,
                            },
                            'InitialAttributes': InitialAttributes,

                        })
            if 'ChipTests' in TestNameDictionary[TestName]:
                self.ResultData['SubTestResultDictList'].append(
                {
                    'Key': 'Chips',
                    'DisplayOptions': {
                        'Order': 1,
                        'Show': True,
                    },
                    'InitialAttributes': {
                        'ModuleVersion': self.Attributes['ModuleVersion'],
                        'Tests': TestNameDictionary[TestName]['ChipTests'],
                        'NumberOfChips': self.Attributes['NumberOfChips'],
                    },
                })

            Index = 2
            if 'Tests' in TestNameDictionary[TestName]:
                for Test in TestNameDictionary[TestName]['Tests']:
                    print "add test: ",Test['Module']
                    InitialAttributes = {
                            'ModuleVersion': self.Attributes['ModuleVersion'],
                            'NumberOfChips': self.Attributes['NumberOfChips'],
                            'StorageKey': Test['Module'],
                    }

                    if 'InitialAttributes' in Test:
                        InitialAttributes.update(Test['InitialAttributes'])

                    self.ResultData['SubTestResultDictList'].append(
                        {
                            'Key': Test['Module'],
                            'DisplayOptions': {
                                'Order': Index,
                                'Show': True,
                                'Width': Test['Width'] if 'Width' in Test else 1,
                            },
                            'InitialAttributes': InitialAttributes,

                        })
                    Index += 1

        self.OpenFileHandle()

    def OpenFileHandle(self):
        self.check_Test_Software()
        fileHandlePath = self.RawTestSessionDataPath + '/commander_%s.root'%self.Attributes['Test']
        try:
            self.FileHandle = ROOT.TFile.Open(fileHandlePath)
        except:
            self.FileHandle = None

        if not self.FileHandle:
            print 'problem to find %s' % fileHandlePath
            XrayRate = None
            if self.RawTestSessionDataPath.endswith('MHz/cm2'):
                XrayRate = self.RawTestSessionDataPath.split('_')[-1].split('MHz/cm2')[0]
                try:
                    XrayRate = int(XrayRate)
                except:
                    XrayRate = None
                self.RawTestSessionDataPath = self.RawTestSessionDataPath[0:-7]

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

        # find pxar logfile of fulltest
        logfilePath = ("%s.log"%fileHandlePath[:-5]) if len(fileHandlePath) > 4 else ''
        self.pxarVersion = None
        if os.path.isfile(logfilePath):
            self.logfilePath = logfilePath
            try:
                with open(logfilePath, 'r') as logFile:
                    for line in logFile:
                        if 'Instanciating API for pxar' in line:
                            posPxar = line.find('pxar')
                            if posPxar >=0:
                                self.pxarVersion = line[posPxar + 5:] if len(line) > posPxar + 5 else '?'
            except:
                pass

    def CustomWriteToDatabase(self, ParentID):
        if self.verbose:
            print 'Write to DB: ',ParentID

        # get IV data
        IVCurveData = {
            'CurrentAtVoltage150V':-1,
            'CurrentAtVoltage100V':-1,
            'RecalculatedCurrentAtVoltage150V':-1,
                'RecalculatedCurrentAtVoltage100V':-1,
                'RecalculatedToTemperature':17,
            'IVSlope':0,
            'IVCurveFilePath':'',
            'TestTemperature':'',
            'IVCurveData':{
                'VoltageList':[],
                'CurrentList':[]
            }
        }
        if self.ResultData['SubTestResults'].has_key('IVCurve'):
            IVCurveTestResultData = self.ResultData['SubTestResults']['IVCurve'].ResultData
            IVCurveData['CurrentAtVoltage150V'] = 0
            # RecalculatedVoltage = 0
            #Check weather there is a recalculated current`
            if IVCurveTestResultData['KeyValueDictPairs'].has_key(
                    'CurrentAtVoltage150V'):
                IVCurveData['CurrentAtVoltage150V'] = float(
                    IVCurveTestResultData['KeyValueDictPairs']['CurrentAtVoltage150V'][
                        'Value'])
                IVCurveData['CurrentAtVoltage150V'] *= IVCurveTestResultData['KeyValueDictPairs']['CurrentAtVoltage150V'].get('Factor',1)
            if IVCurveTestResultData['HiddenData'].has_key(
                    'CurrentAtVoltage100V'):
                IVCurveData['CurrentAtVoltage100V'] = float(
                    IVCurveTestResultData['HiddenData']['CurrentAtVoltage100V'])
            if IVCurveTestResultData['KeyValueDictPairs'].has_key(
                    'recalculatedCurrentAtVoltage150V'):
                IVCurveData['RecalculatedCurrentAtVoltage150V'] = float(
                    IVCurveTestResultData['KeyValueDictPairs'][
                        'recalculatedCurrentAtVoltage150V']['Value'])
                IVCurveData['RecalculatedCurrentAtVoltage150V'] *= self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V'].get('Factor',1)
            else:
                IVCurveData['RecalculatedCurrentAtVoltage150V'] = IVCurveData['CurrentAtVoltage150V']
                IVCurveData['RecalculatedToTemperature'] = IVCurveData['TestTemperature']
                
            if IVCurveTestResultData['HiddenData'].has_key('IVCurveFilePath'):
                IVCurveData['IVCurveFilePath'] = IVCurveTestResultData['HiddenData']['IVCurveFilePath']
            if IVCurveTestResultData['HiddenData'].has_key('TestTemperature'):
                IVCurveData['TestTemperature'] = IVCurveTestResultData['HiddenData']['TestTemperature']
            if IVCurveTestResultData['HiddenData'].has_key('IVCurveData'):
                IVCurveData['IVCurveData'] = IVCurveTestResultData['HiddenData']['IVCurveData']
            
            
            if IVCurveTestResultData['KeyValueDictPairs'].has_key(
                    'recalculatedCurrentAtVoltage100V'):
                IVCurveData['RecalculatedCurrentAtVoltage100V'] = float(
                    IVCurveTestResultData['KeyValueDictPairs'][
                        'recalculatedCurrentAtVoltage100V']['Value'])
                IVCurveData['RecalculatedCurrentAtVoltage100V'] *= self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage100V'].get('Factor',1)
            else:
                IVCurveData['RecalculatedCurrentAtVoltage100V'] = IVCurveData['CurrentAtVoltage100V']
                IVCurveData['RecalculatedToTemperature'] = IVCurveData['TestTemperature']
                
            if IVCurveTestResultData['KeyValueDictPairs'].has_key('Variation'):
                IVCurveData['IVSlope'] = float(
                    IVCurveTestResultData['KeyValueDictPairs']['Variation']['Value'])


        # fill DB row
        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'PixelDefects': None,
            'ROCsLessThanOnePercent': None,
            'ROCsMoreThanOnePercent': None,
            'ROCsMoreThanFourPercent': None,
            'Noise': None,
            'Trimming': None,
            'PHCalibration': None,
            'CurrentAtVoltage150V': None,
            'CurrentAtVoltage100V': None,
            'IVSlope': None,
            'IVCurveFilePath': None,
            'TestTemperature': None,
            'Temperature': None,
            'RelativeModuleFinalResultsPath': os.path.relpath(self.TestResultEnvironmentObject.FinalModuleResultsPath,
                                                              self.TestResultEnvironmentObject.GlobalOverviewPath),
            'FulltestSubfolder': os.path.relpath(self.FinalResultsStoragePath,
                                                 self.TestResultEnvironmentObject.FinalModuleResultsPath),
            # needed for PixelDB
            'AbsModuleFulltestStoragePath': self.TestResultEnvironmentObject.FinalModuleResultsPath,
            'AbsFulltestSubfolder': self.FinalResultsStoragePath,
            'InputTarFile': os.environ.get('TARFILE', None),
            'MacroVersion': os.environ.get('MACROVERSION', None),

            'initialCurrent': None,

            'TestCenter': self.Attributes['TestCenter'],
            'Hostname': self.Attributes['Hostname'],
            'Operator': self.Attributes['Operator'],
        }

        try:
            Row.update({
                'PixelDefects': None,
                'CurrentAtVoltage150V': IVCurveData['CurrentAtVoltage150V'],
                'CurrentAtVoltage100V':IVCurveData['CurrentAtVoltage100V'],
                'IVSlope': IVCurveData['IVSlope'],
                'IVCurveFilePath':IVCurveData['IVCurveFilePath'],
                'TestTemperature':IVCurveData['TestTemperature'],
                'Grade': None,
                'Comments': None,
            })
        except:
            pass
            #test incomplete

        print 'fill row end'

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            print "\x1b[31mSingleTest not supported for global DB\x1b[0m"
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
                        ROCsLessThanOnePercent,
                        ROCsMoreThanOnePercent,
                        ROCsMoreThanFourPercent,
                        CurrentAtVoltage150V,
                        IVSlope,
                        Temperature,
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder,
                        initialCurrent,
                        Comments
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :Grade,
                        :PixelDefects,
                        :ROCsLessThanOnePercent,
                        :ROCsMoreThanOnePercent,
                        :ROCsMoreThanFourPercent,
                        :CurrentAtVoltage150V,
                        :IVSlope,
                        :Temperature,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder,
                        :initialCurrent,
                        :Comments
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid
