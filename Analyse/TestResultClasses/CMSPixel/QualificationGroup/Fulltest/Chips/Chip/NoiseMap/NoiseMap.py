# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='NoiseMap'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    def PopulateResultData(self):

        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)
        ChipNo=self.ParentObject.Attributes['ChipNo']

        try:
            self.ResultData['Plot']['ROOTObject'] = self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['Plot']['ROOTObject_hn'].Clone(self.GetUniqueID())
        except:
            self.ResultData['Plot']['ROOTObject'] = None

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, 200)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')


        self.ResultData['Plot']['Caption'] = 'Noise Map'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()
