# -*- coding: utf-8 -*-
import AbstractClasses
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'SignalTest'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        LogfileName = self.RawTestSessionDataPath + '/adctest.log'
        if LogfileName:
            if os.path.isfile(LogfileName):
                with open(LogfileName) as Logfile:
                    for Line in Logfile:
                        try:
                            signalName = Line.strip().split(' ')[0]
                            signalValue = ' '.join(Line.strip().split(' ')[1:])
                            self.ResultData['KeyValueDictPairs']['signal_' + signalName] = {'Name': signalName, 'Value': signalValue}
                            self.ResultData['KeyList'].append('signal_' + signalName)
                        except:
                            pass