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
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        try:
            self.ParentObject.logfilePaths.sort(key=lambda x: int(x.replace('\\','/').strip('/').split('/')[-2].split('_')[0]))
        except:
            print "Logfiles can not be sorted, all subfolders should be named ***_Name with *** a number."

        for LogfilePath in self.ParentObject.logfilePaths:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key': 'LogfileView',
                    'Module': 'LogfileView',
                    'InitialAttributes': {
                        'LogfilePath' : LogfilePath
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

