import AbstractClasses
import ROOT
import os
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_TestResult'
        self.NameSingle='Module'
        
        self.Title = str(self.Attributes['ModuleID']) + ' ' + self.Attributes['StorageKey']
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Attributes['NumberOfChips'] = 16
        
        if self.Attributes['ModuleVersion'] == 1:
            if self.Attributes['ModuleType'] == 'a':
                self.Attributes['StartChip'] = 0
            elif self.Attributes['ModuleType'] == 'b':
                self.Attributes['StartChip'] = 7
            else:
                self.Attributes['StartChip'] = 0
            
        elif self.Attributes['ModuleVersion'] == 2:
            self.Attributes['StartChip'] = 0
        
        
        
        
        self.ResultData['SubTestResultDictList'] = [
            {
                'Key':'Chips',
                'DisplayOptions':{
                    'GroupWithNext':True,
                    'Order':1,
                },
                'InitialAttributes':{
                    'ModuleVersion':self.Attributes['ModuleVersion'],   
                },
            },
            {
                'Key':'AddressLevelOverview',
                'DisplayOptions':{
                    'Order':2,
                }
            },
            {
                'Key':'BumpBondingMap',
                'DisplayOptions':{
                    'Width':4,
                    'Order':5,
                }
            },
            
            {
                'Key':'VcalThreshold',
                'DisplayOptions':{
                    'Width':4,
                    'Order':3,
                }
            },
        ]
        
        if self.Attributes['IncludeIVCurve']:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'IVCurve',
                    'DisplayOptions':{
                        'Order':8,
                        'Width':3,
                    }
                },
            ]
        else:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'Dummy1',
                    'Module':'Dummy',
                    'DisplayOptions':{
                        'Order':8,
                        'Width':3,
                    }
                },
            ]
        
        self.ResultData['SubTestResultDictList'] += [
            {'Key':'Noise'},
            {'Key':'VcalThresholdWidth'},
            {'Key':'RelativeGainWidth'},
            {'Key':'PedestalSpread'},
        ]
        
        if self.Attributes['ModuleVersion'] == 1:
            self.ResultData['SubTestResultDictList'] += [
                {'Key':'Parameter1'},
            ]
            
        self.ResultData['SubTestResultDictList'] += [
            {
                'Key':'Summary1',
                'DisplayOptions':{
                    'Order':4,
                }
            },
            {
                'Key':'Summary2',
                'DisplayOptions':{
                    'Order':6,
                }
            },
            {
                'Key':'Summary3',
                'DisplayOptions':{
                    'Order':7,
                }
            },
            
        ]
            
        
    def OpenFileHandle(self):
        self.FileHandle = ROOT.TFile.Open(
            self.FullTestResultsPath
            +'/commander_Fulltest.root'
        )
    def PopulateResultData(self):
        
        self.ResultData['Table'] = {
            'HEADER':[
                [
                    'ROC',
                    'Total',
                    'Dead',
                    'Mask',
                    'Bumps',
                    'Trim(Bits)',
                    'Address',
                    'Noise',
                    'Thresh',
                    'Gain',
                    'Ped',
                    'Par1',
                ]
            ],
            'BODY':[],
            'FOOTER':[],
        }
        LinkHTMLTemplate = self.TestResultEnvironmentObject.HtmlParser.getSubpart(
            self.TestResultEnvironmentObject.OverviewHTMLTemplate,
            '###LINK###'
        )
        for i in self.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']:
            self.ResultData['Table']['BODY'].append(
                [
                    self.TestResultEnvironmentObject.HtmlParser.substituteMarkerArray(
                        LinkHTMLTemplate,
                        {
                            '###LABEL###':'Chip '+str(i['TestResultObject'].Attributes['ChipNo']),
                            '###URL###':os.path.relpath(i['TestResultObject'].StoragePath, self.StoragePath)+'/TestResult.html'
                        }
                    ),
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadPixel']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nMaskDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadBumps']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nDeadTrimbits']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nAddressProblems']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nNoisy1Pixel']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nThrDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nGainDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPedDefect']['Value'],
                    i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['nPar1Defect']['Value'],
                ]   
            )
        
        self.FileHandle.Close()
    
        
    
    def CustomWriteToDatabase(self, ParentID):
        if self.ResultData['SubTestResults'].has_key('IVCurve'):
            CurrentAtVoltage150 = float(self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['CurrentAtVoltage150']['Value'])
            IVSlope = float(self.ResultData['SubTestResults']['IVCurve'].ResultData['KeyValueDictPairs']['Variation']['Value'])
        else:
            CurrentAtVoltage150 = 0
            IVSlope = 0
            
        Row = {
            'ModuleID' : self.Attributes['ModuleID'],
            'TestDate': self.Attributes['TestDate'],
            'TestType': self.Attributes['TestType'],
            'Grade':  self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['Grade']['Value'],
            'PixelDefects': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['DeadPixels']['Value'],
            'ROCsMoreThanOnePercent': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['BadRocs']['Value'],
            'Noise': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['NoisyPixels']['Value'],
            'Trimming': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['TrimProblems']['Value'],
            'PHCalibration': self.ResultData['SubTestResults']['Summary1'].ResultData['KeyValueDictPairs']['PHGainDefects']['Value'],
            'CurrentAtVoltage150': CurrentAtVoltage150,
            'IVSlope': IVSlope,
            'Temperature': self.ResultData['SubTestResults']['Summary2'].ResultData['KeyValueDictPairs']['TempC']['Value'],
            'StorageFolder':os.path.relpath(self.TestResultEnvironmentObject.TestResultsPath, self.TestResultEnvironmentObject.OverviewPath),
            'Comments': '',
            'nCycles': None,
            'CycleTempLow': None,
            'CycleTempHigh':None,
        }
        if self.TestResultEnvironmentObject.Configuration['Database']['UseGlobal']:
            pass
        else:
            with self.TestResultEnvironmentObject.LocalDBConnection:
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute('DELETE FROM ModuleTestResults WHERE ModuleID = :ModuleID AND TestType=:TestType',Row)
                self.TestResultEnvironmentObject.LocalDBConnectionCursor.execute(
                    '''INSERT INTO ModuleTestResults 
                    (
                        ModuleID,
                        TestDate,
                        TestType,
                        Grade,
                        PixelDefects,
                        ROCsMoreThanOnePercent,
                        Noise,
                        Trimming,
                        PHCalibration,
                        CurrentAtVoltage150,
                        IVSlope,
                        Temperature,
                        StorageFolder,
                        Comments,
                        nCycles,
                        CycleTempLow,
                        CycleTempHigh
                    )
                    VALUES (
                        :ModuleID,
                        :TestDate,
                        :TestType,
                        :Grade,
                        :PixelDefects,
                        :ROCsMoreThanOnePercent,
                        :Noise,
                        :Trimming,
                        :PHCalibration,
                        :CurrentAtVoltage150,
                        :IVSlope,
                        :Temperature,
                        :StorageFolder,
                        :Comments,
                        :nCycles,
                        :CycleTempLow,
                        :CycleTempHigh
                    )
                    ''', Row)
                return self.TestResultEnvironmentObject.LocalDBConnectionCursor.lastrowid
            
    
