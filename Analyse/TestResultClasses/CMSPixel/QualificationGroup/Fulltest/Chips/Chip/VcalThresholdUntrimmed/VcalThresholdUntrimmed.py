# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_VcalThresholdUntrimmed_TestResult'
        self.NameSingle='VcalThresholdUntrimmed'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'



    def PopulateResultData(self):

        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)
        ChipNo=self.ParentObject.Attributes['ChipNo']

        try:
            self.ResultData['Plot']['ROOTObject'] = self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['Plot']['ROOTObject_ht'].Clone(self.GetUniqueID())
        except:
            self.ResultData['Plot']['ROOTObject'] = None

        pxarfit = False
        if self.ResultData['Plot']['ROOTObject'] is None or ('NoDatFile' in self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['HiddenData'] and self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['HiddenData']['NoDatFile']):
            HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
            histname = HistoDict.get(self.NameSingle, 'ThresholdMap')
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo).Clone(self.GetUniqueID())
            print "error: Scurve .dat file not found, try to use pxar histogram from root file instead! histogram: ", histname
            if self.ResultData['Plot']['ROOTObject']:
                print "found!"
                self.ResultData['KeyValueDictPairs']['fit'] = {
                        'Label' : 'Fit',
                        'Value': 'pxar',
                    }
                self.ResultData['KeyList'].append('fit')
                pxarfit = True

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['HiddenData']['htmin'], self.ParentObject.ResultData['SubTestResults']['SCurveWidths'].ResultData['HiddenData']['htmax'])
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            if pxarfit:
                self.ResultData['Plot']['ROOTObject'].SetTitle("fit and histogram taken from pxar!!!")
            self.ResultData['Plot']['ROOTObject'].Draw('colz')



        self.ResultData['Plot']['Caption'] = 'Vcal Threshold Untrimmed'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()
