import os
import ROOT
import glob
import math

import AbstractClasses
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

from AbstractClasses.GeneralTestResult import GeneralTestResult
import subprocess

class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_LeakageCurrentPON_TestResult'
        self.NameSingle = 'LeakageCurrentPON'
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
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

        self.ResultData['SubTestResultDictList'] = [
            {
                'Key': 'LeakageCurrent',
                'DisplayOptions': {
                    'Width' : 2,
                    'Order': 20
                },
                'InitialAttributes': {
                    'ModuleVersion': self.Attributes['ModuleVersion'],
                },
            },
        ]
        self.Attributes['TestedObjectType'] = 'LeakageCurrentPON'

    def OpenFileHandle(self):

        testPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_[lL]eakageCurrentPON_*')
        for Path in testPaths:
            FolderName = os.path.basename(Path)
            self.FileHandle = open(self.RawTestSessionDataPath+"/"+FolderName + "/leakageCurrent.log", 'r')
            temperature = FolderName.split("_")[-1]

            if temperature[0] == "p":
                self.Attributes['Temperature'] = float(temperature[1:])
            elif temperature[0] == "m":
                self.Attributes['Temperature'] = -float(temperature[1:])
            else:
                self.Attributes['Temperature'] = 17.0

            break

    def PopulateResultData(self):
        self.FileHandle.close()

        self.ResultData['KeyValueDictPairs'] = {
            'LeakageCurrent': {
                "Value": self.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['LeakageCurrent']['Value'],
                "Label": 'Leakage Current',
                "Unit": "A",
            },'Voltage': {
                "Value": self.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['Voltage']['Value'],
                "Label": 'Voltage',
                "Unit": "V",
            },
        }


    def CustomWriteToDatabase(self, ParentID):
        print 'Write to DB: ',ParentID

        leakageCurrent = float(self.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['LeakageCurrent']['Value'])
        gradeMapping = {1: 'A', 2: 'B', 3: 'C'}

        grade = 1
        # grading parameters in uA
        if self.TestResultEnvironmentObject.GradingParameters.has_key('leakageCurrentPON_B'):
            thr_B = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_B']
            if abs(leakageCurrent) > abs(thr_B)*1.e-6:
                grade = 2
        if self.TestResultEnvironmentObject.GradingParameters.has_key('leakageCurrentPON_C'):
            thr_C = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_C']
            if abs(leakageCurrent) > abs(thr_C)*1.e-6:
                grade = 3

        print 'fill row'
        Row = {
            'ModuleID': self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
            'RelativeModuleFinalResultsPath': os.path.relpath(self.TestResultEnvironmentObject.FinalModuleResultsPath,
                                                              self.TestResultEnvironmentObject.GlobalOverviewPath),
            'FulltestSubfolder': os.path.relpath(self.FinalResultsStoragePath,
                                                 self.TestResultEnvironmentObject.FinalModuleResultsPath),
            'initialCurrent': leakageCurrent,
            'Temperature': self.Attributes['Temperature'],
            'Grade': gradeMapping[grade]
        }
        print 'fill row end'

        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            pass
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
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder,
                        initialCurrent,
                        Temperature,
                        Grade
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder,
                        :initialCurrent,
                        :Temperature,
                        :Grade
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid

       
