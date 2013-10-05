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
#        self.Attributes['NumberOfChips'] = 16
#        
#        if self.Attributes['ModuleVersion'] == 1:
#            if self.Attributes['ModuleType'] == 'a':
#                self.Attributes['StartChip'] = 0
#            elif self.Attributes['ModuleType'] == 'b':
#                self.Attributes['StartChip'] = 7
#            else:
#                self.Attributes['StartChip'] = 0
#            
#        elif self.Attributes['ModuleVersion'] == 2:
#            self.Attributes['StartChip'] = 0
        
        
        
        
#        self.ResultData['SubTestResultDictList'] = [
#            {
#                'Key':'Chips',
#                'DisplayOptions':{
#                    'GroupWithNext':True,
#                    'Order':1,
#                },
#                'InitialAttributes':{
#                    'ModuleVersion':self.Attributes['ModuleVersion'],   
#                },
#            },
#            {
#                'Key':'AddressLevelOverview',
#                'DisplayOptions':{
#                    'Order':2,
#                }
#            },
#            {
#                'Key':'BumpBondingMap',
#                'DisplayOptions':{
#                    'Width':4,
#                    'Order':5,
#                }
#            },
#            
#            {
#                'Key':'VcalThreshold',
#                'DisplayOptions':{
#                    'Width':4,
#                    'Order':3,
#                }
#            },
#        ]
        
#        if self.Attributes['IncludeIVCurve']:
#            self.ResultData['SubTestResultDictList'] += [
#                {
#                    'Key':'IVCurve',
#                    'DisplayOptions':{
#                        'Order':8,
#                        'Width':3,
#                    }
#                },
#            ]
#        else:
#            self.ResultData['SubTestResultDictList'] += [
#                {
#                    'Key':'Dummy1',
#                    'Module':'Dummy',
#                    'DisplayOptions':{
#                        'Order':8,
#                        'Width':3,
#                    }
#                },
#            ]
        
#        self.ResultData['SubTestResultDictList'] += [
#            {'Key':'Noise'},
#            {'Key':'VcalThresholdWidth'},
#            {'Key':'RelativeGainWidth'},
#            {'Key':'PedestalSpread'},
#        ]
        
#        if self.Attributes['ModuleVersion'] == 1:
#            self.ResultData['SubTestResultDictList'] += [
#                {'Key':'Parameter1'},
#            ]
            
#        self.ResultData['SubTestResultDictList'] += [
#            {
#                'Key':'Summary1',
#                'DisplayOptions':{
#                    'Order':4,
#                }
#            },
#            {
#                'Key':'Summary2',
#                'DisplayOptions':{
#                    'Order':6,
#                }
#            },
#            {
#                'Key':'Summary3',
#                'DisplayOptions':{
#                    'Order':7,
#                }
#            },
#            
#        ]
            
        
    def OpenFileHandle(self):
        self.FileHandle = ConfigParser.ConfigParser()
        fileName = self.RawTestSessionDataPath+'/elComandante.ini'
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
#        self.ResultData['Table'] = {
#            'HEADER':[
#                [
#                    'Test Name',
#                    'nCycles',
#                    'CycleTempLow',
#                    'CycleTempHigh',
#                ]
#            ],
#            'BODY':[],
#            'FOOTER':[],
#        }
#        LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
#            self.TestResultEnvironmentObject.OverviewHTMLTemplate,
#            '###LINK###'
#        )
        #for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']:
#        self.ResultData['Table']['BODY'].append(
#            [
#                self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
#                    LinkHTMLTemplate,
#                    {
#                        '###LABEL###':'TemperatureCycle',
#                        #i['TestResultObject'].FinalResultsStoragePath, self.FinalResultsStoragePath)+'/TestResult.html'
#                        '###URL###':os.path.relpath(self.FinalResultsStoragePath, self.FinalResultsStoragePath)+'/TestResult.html'
#                    }
#                ),
#                self.Attributes['nCycles'],
#                self.Attributes['CycleTempLow'],
#                self.Attributes['CycleTempHigh'],
#            ]   
#        )
        del self.FileHandle
#        self.FileHandle.Close()
    
        
    
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
            
    
