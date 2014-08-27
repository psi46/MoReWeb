# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
import datetime
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Summary2_TestResult'
        self.NameSingle='Summary2'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Summary 2'

        
    def PopulateResultData(self):
        try:
            test_date = self.Attributes['TestDate'].split()[0]
            test_date = datetime.datetime.fromtimestamp(float(test_date)).strftime("%Y-%m-%d")
        except ValueError as e:
            print 'testdate',self.Attributes['TestDate']
            raise e
        self.ResultData['KeyValueDictPairs'] = {
            'TestDate': {
                'Value':test_date,
                'Label':'Test Date'
            },
            'TestTime': {
                'Value':datetime.datetime.fromtimestamp(float(self.Attributes['TestDate'])).strftime("%H:%m"), 
                'Label':'Test Time'
            },
            'TempC': {
                'Value':'{0:1.0f}'.format(self.ParentObject.Attributes['TestTemperature']),
                'Unit':'°C',
                'Label':'Temparature'
            },
            'TrimPHCal':{
                'Value':'yes / yes', 
                'Label':'Trim / phCal'
            },
            'TermCycl':{
                'Value':'yes', 
                'Label':'Term. Cycl.'
            },
            'TBM1':{
                'Value':'ok', 
                'Label':'TBM1'
            },
            'TBM2':{
                'Value':'ok', 
                'Label':'TBM2'
            },
        
        }
        
        self.ResultData['KeyList'] = ['TestDate','TestTime','TempC','TrimPHCal','TermCycl', 'TBM1', 'TBM2']

