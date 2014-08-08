# -*- coding: utf-8 -*-
import AbstractClasses
import ROOT
import os
import ConfigParser
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_TemperatureCycle_TestResult'
        self.NameSingle='TemperatureCycle'
        
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        
    def OpenFileHandle(self):
        self.FileHandle = ConfigParser.ConfigParser()
        fileName = self.RawTestSessionDataPath+'/elComandante.ini'
        if not os.path.isfile(fileName):
            fileName = self.RawTestSessionDataPath+'/Tests.ini'
#        print 'open ConfigFile "%s"'%fileName 
        self.FileHandle.read(fileName)

    def PopulateResultData(self):
        self.ResultData['KeyValueDictPairs']['nCycles'] = {'Value': self.FileHandle.get('Cycle','nCycles'), 'Unit': '#',}
        self.ResultData['KeyValueDictPairs']['CycleTempHigh'] ={
                                                                'Value': self.FileHandle.get('Cycle','highTemp'),
                                                                'Unit': '℃',
                                                                }
        self.ResultData['KeyValueDictPairs']['CycleTempLow'] = {
                                                                'Value': self.FileHandle.get('Cycle','lowTemp'),
                                                                'Unit': '℃',
                                                                }
        self.ResultData['KeyList'] = ['nCycles','CycleTempLow','CycleTempHigh']

        del self.FileHandle
    
        
    
    def CustomWriteToDatabase(self, ParentID):
        print "Set Row"           
        Row = {                     
            'ModuleID' : self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'QualificationType': self.ParentObject.Attributes['QualificationType'],
#            'Grade': None,
#            'PixelDefects': None,
#            'ROCsMoreThanOnePercent': None,
#            'Noise': None,
#            'Trimming': None,
#            'PHCalibration': None,
#            'CurrentAtVoltage150': None,
#            'IVSlope': None,
#            'Temperature': None,
            'RelativeModuleFinalResultsPath':os.path.relpath(self.TestResultEnvironmentObject.FinalModuleResultsPath, self.TestResultEnvironmentObject.GlobalOverviewPath),
            'FulltestSubfolder':os.path.relpath(self.FinalResultsStoragePath, self.TestResultEnvironmentObject.FinalModuleResultsPath),
            'Comments': '',
            'nCycles': self.ResultData['KeyValueDictPairs']['nCycles']['Value'],
            'CycleTempLow': self.ResultData['KeyValueDictPairs']['CycleTempLow']['Value'],
            'CycleTempHigh':self.ResultData['KeyValueDictPairs']['CycleTempHigh']['Value'],
        }
        
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            print 'use global DB'
            pass
        else:
            with self.TestResultEnvironmentObject.LocalDBConnection:
                print 'Delete from DB'
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute('DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType=:TestType AND QualificationType=:QualificationType AND TestDate <= :TestDate',Row)
                print 'Insert into DB'
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    '''INSERT INTO ModuleTestResults 
                     (
                        ModuleID,
                        TestDate,
                        TestType,
                        QualificationType,
                        RelativeModuleFinalResultsPath,
                        FulltestSubfolder,
                        nCycles,
                        CycleTempLow,
                        CycleTempHigh
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :QualificationType,
                        :RelativeModuleFinalResultsPath,
                        :FulltestSubfolder,
                        :nCycles,
                        :CycleTempLow,
                        :CycleTempHigh
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid
            
    
