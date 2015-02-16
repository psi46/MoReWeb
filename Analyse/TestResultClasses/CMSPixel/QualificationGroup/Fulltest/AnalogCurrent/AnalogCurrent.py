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
            self.ResultData['Plot']['ROOTObject'] = self.ParentObject.ResultData['SubTestResults']['DigitalCurrent'].get_Current_Graph(object)
            print 'BLA', self.ResultData['Plot']['ROOTObject']
            self.ResultData['Plot']['Graph'] = object.Clone(self.GetUniqueID())
            print self.ResultData['Plot']['ROOTObject']

            if self.ResultData['Plot']['ROOTObject']:
                self.Canvas.Clear()
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Time / s")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("analog current / A")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw('APL')
            if self.SavePlotFile:
                print 'SavePlotFile', self.SavePlotFile
                self.Canvas.SaveAs(self.GetPlotFileName())
            self.ResultData['Plot']['Enabled'] = 1
            self.Title = 'Analog Current'
            self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
            print self.GetPlotFileName()
        except Exception as e:
            print e