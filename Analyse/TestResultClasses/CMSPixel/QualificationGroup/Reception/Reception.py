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
        self.Name = 'CMSPixel_QualificationGroup_Reception_TestResult'
        self.NameSingle = 'Reception'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = self.nTotalChips
        self.Attributes['StartChip'] = 0
        self.Attributes['ModuleVersion'] = 1
        self.Attributes['isDigital'] = 1

        self.AddCommentsToKeyValueDictPairs = True
        self.ResultData['SubTestResultDictList'] = [
            {
                'Key': 'Chips',
                'DisplayOptions': {
                    'Order': 1,
                    'Show': True,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },  
            {
                'Key': 'Grading',
                'DisplayOptions': {
                    'Order': 15,
                    'Width': 1,
                    'Show': True,
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },
        ]

        if self.Attributes['IncludeIVCurve']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key': 'IVCurve',
                    'DisplayOptions': {
                        'Order': 30,
                        'Width': 1,
                    }
                },
            ]

        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'BumpBondingMap',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 40,
                },
                'InitialAttributes': {
                    'StorageKey': 'BumpBondingMap'
                }
            }
        ]
        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'BumpBondingProblems',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 20,
                },
                'InitialAttributes': {
                    'StorageKey': 'BumpBondingProblems'
                }
            }
        ]
        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'PixelMap',
                'DisplayOptions': {
                    'Width': 4,
                    'Order': 5,
                },
                'InitialAttributes': {
                    'StorageKey': 'BumpBondingMap'
                }
            }
        ]

    def OpenFileHandle(self):
        self.check_Test_Software()
        fileHandlePath = self.RawTestSessionDataPath + '/commander_Reception.root'
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
            from PixelDB import *
            # modified by Tommaso
            #
            # try and speak directly with PixelDB
            #

#            fake = int(os.environ.get('FAKE',1))

#            insertedID=7
            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()
            
#            if (0 == 0):
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
