# -*- coding: utf-8 -*-
import ROOT
import array
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_AnalogCurrent_TestResult'
        self.NameSingle='AnalogCurrent'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        try:
            histname = self.ParentObject.HistoDict.get(self.NameSingle, 'AnalogCurrent')
            print histname
            object = HistoGetter.get_histo(self.ParentObject.FileHandle, histname)
            print object
            self.ResultData['Plot']['ROOTHisto'] = object
        except Exception as e:
            print e
            raise e
        self.ParentObject.ResultData['SubTestResults']['DigitalCurrent'].SpecialPopulateResultData(self,{'name':'Analog Current'})