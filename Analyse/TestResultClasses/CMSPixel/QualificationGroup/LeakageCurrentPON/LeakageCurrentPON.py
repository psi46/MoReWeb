import os
import ROOT
import glob

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

        testPaths = glob.glob(self.RawTestSessionDataPath+'/0[0-9][0-9]_leakageCurrentPON_*')
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
                    
        print "LeakageCurrentPON::OpenFileHandle"

    def PopulateResultData(self):
        self.FileHandle.close()

        self.ResultData['KeyValueDictPairs'] = {
            'LeakageCurrent': {
                "Value": self.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['LeakageCurrent']['Value'],
                "Label": 'LeakageCurrentPeak',
                "Unit": "",
            },'Voltage': {
                "Value": self.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['Voltage']['Value'],
                "Label": 'LeakageCurrentPeakTime',
                "Unit": "",
            },
        }


    def CustomWriteToDatabase(self, ParentID):
        print 'Write to DB: ',ParentID

        leakageCurrent = self.ResultData['SubTestResults']['LeakageCurrent'].ResultData['KeyValueDictPairs']['LeakageCurrent']['Value']

        inputTemp = 273.15 + self.Attributes['Temperature']
        outputTemp = 273.15 + 17.0
        Eef = 1.21
        kB = 8.62e-5
        exp = Eef / 2 / kB * (1 / inputTemp - 1 / outputTemp)
        leakageCurrentRecalculated = leakageCurrent * outputTemp ** 2 / inputTemp ** 2 * math.exp(exp)

        grade = 'A'
        print repr(self.TestResultEnvironmentObject.GradingParameters)

        if self.TestResultEnvironmentObject.GradingParameters.has_key('leakageCurrentPON_B'):
            thr_B = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_B']
            if abs(leakageCurrent) > abs(thr_B):
                grade = 'B'
        if self.TestResultEnvironmentObject.GradingParameters.has_key('leakageCurrentPON_C'):
            thr_C = self.TestResultEnvironmentObject.GradingParameters['leakageCurrentPON_C']
            if abs(leakageCurrent) > abs(thr_C):
                grade = 'C'

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
            'CurrentAtVoltage150V': leakageCurrent,
            'RecalculatedVoltage': leakageCurrentRecalculated,  #recalculated current!
            'Temperature': self.Attributes['Temperature'],
            'Grade': grade,
            'Comments': '',
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
                        CurrentAtVoltage150V,
                        RecalculatedVoltage,
                        Temperature,
                        Grade,
                        Comments
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder,
                        :CurrentAtVoltage150V,
                        :RecalculatedVoltage,
                        :Temperature,
                        :Grade,
                        :Comments
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid

       
