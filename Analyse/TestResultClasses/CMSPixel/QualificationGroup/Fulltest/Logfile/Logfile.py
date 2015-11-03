# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

import ROOT
import datetime
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='Logfile'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['SubTestResultDictList'] += [
            {
                'Key': 'LogfileView',
                'Module': 'LogfileView',
                'InitialAttributes': {
                },
                'DisplayOptions': {
                    'Order': 100,
                    'Width': 5,
                    'Show': True,
                }
            },
        ]

    def PopulateResultData(self):
        pass

