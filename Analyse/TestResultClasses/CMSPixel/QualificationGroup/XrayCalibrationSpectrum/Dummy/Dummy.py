# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Xray_Dummy_TestResult'
        self.NameSingle='Dummy'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = '_'

        
    def PopulateResultData(self):
        pass
