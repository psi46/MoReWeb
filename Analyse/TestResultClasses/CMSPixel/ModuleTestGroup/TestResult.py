import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_TestResult'
        self.NameSingle='ModuleTestGroup'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Module Test Group '+self.Attributes['ModuleID']
        
        if self.Attributes['TestType'] == 'FullQualification':
            self.ResultData['SubTestResultDictList'] = [
                {
                    'Key':'ModuleFulltest_p17',
                    'Module':'Module',
                    'InitialAttributes':{
                        'StorageKey':    'ModuleFulltest_p17',
                        'TestResultSubDirectory': '004_Fulltest_p17',
                        'IncludeIVCurve':True,
                        'IVCurveSubDirectory':    '005_IV_p17',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'p17',
                        'TestTemperature':17,
                    },
                    'DisplayOptions':{
                        'Order':3        
                    }
                },
                {
                    'Key':'ModuleFulltest_m10_1',
                    'Module':'Module',
                    'InitialAttributes':{
                        'StorageKey':    'ModuleFulltest_m10_1',
                        'TestResultSubDirectory': '001_Fulltest_m10',
                        'IncludeIVCurve':False,
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'m10_1',
                        'TestTemperature':-10,
                    },
                    'DisplayOptions':{
                        'Order':1        
                    }
                },
                {
                    'Key':'ModuleFulltest_m10_2',
                    'Module':'Module',
                    'InitialAttributes':{
                        'StorageKey':    'ModuleFulltest_m10',
                        'TestResultSubDirectory': '002_Fulltest_m10',
                        'IncludeIVCurve':True,
                        'IVCurveSubDirectory':    '003_IV_m10',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'m10_2',
                        'TestTemperature':-10,
                        'recalculateCurrentTo': 17
                    },
                    'DisplayOptions':{
                        'Order':2        
                    }
                },
            ]

        elif self.Attributes['TestType'] == '2TempQualification':
            self.ResultData['SubTestResultDictList'] = [
                {
                    'Key':'ModuleFulltest_p17',
                    'Module':'Module',
                    'InitialAttributes':{
                        'StorageKey':    'ModuleFulltest_p17',
                        'TestResultSubDirectory': '000_Fulltest_p17',
                        'IncludeIVCurve':True,
                        'IVCurveSubDirectory':    '001_IV_p17',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'p17',
                        'TestTemperature':17,
                    },
                    'DisplayOptions':{
                        'Order':3        
                    }
                },
                {
                    'Key':'ModuleFulltest_m10_2',
                    'Module':'Module',
                    'InitialAttributes':{
                        'StorageKey':    'ModuleFulltest_m10',
                        'TestResultSubDirectory': '002_Fulltest_m10',
                        'IncludeIVCurve':True,
                        'IVCurveSubDirectory':    '003_IV_m10',
                        'ModuleID':self.Attributes['ModuleID'],
                        'ModuleVersion':self.Attributes['ModuleVersion'],
                        'ModuleType':self.Attributes['ModuleType'],
                        'TestType':'m10',
                        'TestTemperature':-10,
                        'recalculateCurrentTo': 17
                    },
                    'DisplayOptions':{
                        'Order':2        
                    }
                },
            ]
        
    def PopulateResultData(self):
        ModuleResultOverviewObject = AbstractClasses.ModuleResultOverview.ModuleResultOverview(self.TestResultEnvironmentObject)
        ModuleResultOverviewObject.StoragePath = self.StoragePath
        self.ResultData['Table'] = ModuleResultOverviewObject.TableData(self.Attributes['ModuleID'],self.Attributes['TestDate'])
        
    
