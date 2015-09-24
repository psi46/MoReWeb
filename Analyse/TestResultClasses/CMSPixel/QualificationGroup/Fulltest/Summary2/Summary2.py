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

        TBM1status = 'ok'
        TBM2status = 'ok'

        try:
            corea_basea = self.ParentObject.ResultData['SubTestResults']['TBM'].ResultData['KeyValueDictPairs']['Core0a_basea']['Value']
            coreb_basea = self.ParentObject.ResultData['SubTestResults']['TBM'].ResultData['KeyValueDictPairs']['Core0b_basea']['Value']
            corea_basee = self.ParentObject.ResultData['SubTestResults']['TBM'].ResultData['KeyValueDictPairs']['Core0a_basee']['Value']
            coreb_basee = self.ParentObject.ResultData['SubTestResults']['TBM'].ResultData['KeyValueDictPairs']['Core0b_basee']['Value']

            TBM1status = "ok, %s %s"%(corea_basee, corea_basea)
            TBM2status = "ok, %s %s"%(coreb_basee, coreb_basea)

        except:
            pass

        try:
            TestDuration = self.ParentObject.ResultData['SubTestResults']['DigitalCurrent'].ResultData['KeyValueDictPairs']['Duration']['Value']
        except:
            try:
                TestDuration = self.ParentObject.ResultData['SubTestResults']['AnalogCurrent'].ResultData['KeyValueDictPairs']['Duration']['Value']
            except:
                TestDuration = ''

        self.ResultData['KeyValueDictPairs'] = {
            'TestDate': {
                'Value':test_date,
                'Label':'Test Date'
            },
            'TestTime': {
                'Value':datetime.datetime.fromtimestamp(float(self.Attributes['TestDate'])).strftime("%H:%M"), 
                'Label':'Test Time'
            },
            'TestDuration': {
                'Value': TestDuration,
                'Label':'Test Duration'
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
                'Value': TBM1status, 
                'Label':'TBM1'
            },
            'TBM2':{
                'Value': TBM2status, 
                'Label':'TBM2'
            },
        
        }
        
        self.ResultData['KeyList'] = ['TestDate','TestTime', 'TestDuration', 'TempC','TrimPHCal','TermCycl', 'TBM1', 'TBM2']

        if self.ParentObject.pxarVersion:
            self.ResultData['KeyValueDictPairs']['PxarVersion'] = {'Label': 'pXar', 'Value': self.ParentObject.pxarVersion.replace("~","\n")}
            self.ResultData['KeyList'].append('PxarVersion')




