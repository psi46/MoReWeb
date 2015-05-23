import os
import sys
import ROOT
import os.path
import glob

import AbstractClasses
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

from AbstractClasses.GeneralTestResult import GeneralTestResult
import subprocess

class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_TestResult'
        self.NameSingle = 'XRayHRQualification'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = self.nTotalChips
        #self.MergePyxarData()

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
        
        self.Attributes['Rates'] = []
        self.Attributes['ROOTFiles'] = {}
        self.Attributes['SCurvePaths'] = {}
        for Rate in self.TestResultEnvironmentObject.XRayHRQualificationConfiguration['Rates']:
            
            HREfficiencyPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HREfficiency_{:d}/'.format(Rate))
            HRDataPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRData_{:d}'.format(Rate))
            HRSCurvesPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_HRScurves_{:d}'.format(Rate))
            if len(HREfficiencyPaths) and len(HRDataPaths) and len(HRSCurvesPaths):
               self.Attributes['Rates'].append(Rate)
               self.Attributes['ROOTFiles']['HREfficiency_{:d}'.format(Rate)] = ROOT.TFile.Open(HREfficiencyPaths[0]+'/pxar.root')
               self.Attributes['ROOTFiles']['HRData_{:d}'.format(Rate)] = ROOT.TFile.Open(HREfficiencyPaths[0]+'/pxar.root')
               self.Attributes['SCurvePaths']['HRSCurves_{:d}'.format(Rate)] = HRSCurvesPaths[0]
               

        self.ResultData['SubTestResultDictList'] = [
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

            # {
                # 'Key': 'BumpBondingMap',
                # 'DisplayOptions': {
                    # 'Width': 4,
                    # 'Order': 5,
                # }
            # },
            # {
                # 'Key': 'VcalThreshold',
                # 'DisplayOptions': {
                    # 'Width': 4,
                    # 'Order': 3,
                # }
            # },
        ]
       

    def OpenFileHandle(self):
        pass

    def PopulateResultData(self):
        pass

    def CustomWriteToDatabase(self, ParentID):
        if self.verbose:
            print 'Write to DB: ',ParentID

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
            'nNoisyPixels':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'],
            
            'TestCenter': self.Attributes['TestCenter'],
            'Hostname': self.Attributes['Hostname'],
            'Operator': self.Attributes['Operator'],
            #
            # added by Felix for the new Overview Table
            #
            # for A/B/C sub gradings
            
            'NoiseNGradeA':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeAROCs'][
                    'Value'],
            'NoiseNGradeB':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeBROCs'][
                    'Value'],
            'NoiseNGradeC':
                self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoiseGradeCROCs'][
                    'Value'],

        }
        print 'fill row end'
        if False and self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            from PixelDB import *
            pdb = PixelDBInterface(operator="tommaso", center="pisa")
            pdb.connectToDB()
            
            
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


