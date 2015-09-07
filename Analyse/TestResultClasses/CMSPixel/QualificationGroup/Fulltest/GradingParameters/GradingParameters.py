# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import ConfigParser
import ROOT
import datetime

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='GradingParameters'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        Configuration = ConfigParser.ConfigParser()
        Configuration.read(['Configuration/GradingParameters.cfg'])
        DefaultConfiguration = ConfigParser.ConfigParser()
        DefaultConfiguration.read(['Configuration/GradingParameters.cfg.default'])

        ModifiedGrading = False
        self.ResultData['KeyValueDictPairs']['ModifiedGrading'] = {'Label': 'Modified Grading', 'Value': 'False'}
        self.ResultData['KeyList'] = ['ModifiedGrading']

        try:
            for i in self.TestResultEnvironmentObject.GradingParameters: 
                GradingDefault = DefaultConfiguration.get('GradingParameters', i).strip()
                Grading = Configuration.get('GradingParameters', i).strip()
                if Grading != GradingDefault:
                    ModifiedGrading = True
                    self.ResultData['KeyValueDictPairs']['GradingParameters_%s'%i] = {'Label': i, 'Value': '%s => %s'%(GradingDefault, Grading)}
                    self.ResultData['KeyList'].append('GradingParameters_%s'%i)

            if ModifiedGrading:
                self.ResultData['KeyValueDictPairs']['ModifiedGrading']['Value'] = 'True'
        except:
            self.ResultData['KeyValueDictPairs']['ModifiedGrading']['Value'] = '?'

