# -*- coding: utf-8 -*-
import AbstractClasses
import datetime
from math import floor
import glob

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'TestEnvironment'
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_%s_TestResult'%self.NameSingle
        self.Title = 'Setup'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):

        try:
            pXarVersion = self.ParentObject.ResultData['SubTestResults']['Logfile'].ResultData['KeyValueDictPairs']['pXar']['Value']
        except:
            pXarVersion = ''

        try:
            FWVersion = self.ParentObject.ResultData['SubTestResults']['Logfile'].ResultData['KeyValueDictPairs']['DTB_FW']['Value']
        except:
            FWVersion = ''

        try:
            test_center = self.ParentObject.ResultData['SubTestResults']['ConfigFiles'].ResultData['KeyValueDictPairs']['TestCenter']['Value']
        except:
            test_center = ''

        # Test date and duration
        try:
            test_date = self.Attributes['TestDate'].split()[0]
            test_date = datetime.datetime.fromtimestamp(float(test_date)).strftime("%Y-%m-%d")
        except ValueError as e:
            print 'testdate',self.Attributes['TestDate']
            raise e

        try:
            logFileSearchString = self.RawTestSessionDataPath + "/logfiles/elComandante.log"
            logFiles = glob.glob(logFileSearchString)
            if len(logFiles) == 1:
                EndSectionFound = False
                with open(logFiles[0]) as logFile:
                    for Line in logFile:
                        if 'Finished all tests' in Line:
                            EndSectionFound = True
                        if EndSectionFound and Line.strip()[0:5] == 'total':
                            LineItems = [x for x in Line.replace('\t',' ').replace('\n',' ').split(' ') if len(x.strip()) > 0]
                            pMins = LineItems.index('min')
                            pSecs = LineItems.index('sec')
                            Mins = int(LineItems[pMins-1])
                            Secs = int(LineItems[pSecs-1])

                            Hours = floor(Mins/60)
                            Mins = Mins - Hours*60

                            TestDuration = "{H:1.0f}:{M:1.0f}:{S:1.0f}".format(H=Hours, M=Mins, S=Secs)
                            break

            else:
                print "no 'elComandante.log' file found!"
                raise
        except:
            raise
            TestDuration = '-'

        self.ResultData['KeyValueDictPairs'] = {
            'TestCenter': {
                'Value': test_center,
                'Label':'Test Center'
            },
            'TestDate': {
                'Value': test_date,
                'Label':'Test Date'
            },
            'TestTime': {
                'Value': datetime.datetime.fromtimestamp(float(self.Attributes['TestDate'])).strftime("%H:%M"),
                'Label':'Test Time'
            },
            'TestDuration': {
                'Value': TestDuration,
                'Label':'Duration'
            },
            'TempC': {
                'Value':'{0:1.0f}'.format(self.ParentObject.Attributes['TestTemperature']),
                'Unit':'°C',
                'Label':'Temparature'
            },
            'pXar': {
                'Value': pXarVersion,
                'Label': 'pXar version',
            },
            'DTB_FW': {
                'Value': FWVersion,
                'Label': 'DTB FW',
            },
        }

        self.ResultData['KeyList'] = ['TestCenter', 'TestDate', 'TestTime', 'TestDuration', 'pXar', 'DTB_FW']


