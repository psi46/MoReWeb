# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_VcalThresholdTrimmedMap_TestResult'
        self.NameSingle='VcalThresholdTrimmedMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.ThrDefectList = set()
        self.chipNo = self.ParentObject.Attributes['ChipNo']



    def PopulateResultData(self):


        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)
        ChipNo=self.ParentObject.Attributes['ChipNo']

        try:
            DeadPixelList = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        except:
            DeadPixelList = ()
            print "warning: could not find pixel alive map, cannot distinguish threshold defects from dead pixels!"

        ChipNo = self.ParentObject.Attributes['ChipNo']
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'ThresholdMapTrimmed')
        ThresholdMap =  HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle,histname,rocNo=ChipNo).Clone(self.GetUniqueID())
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows)

        for col in range(0, ThresholdMap.GetNbinsX()):
            for row in range(0, ThresholdMap.GetNbinsY()):
                threshold = ThresholdMap.GetBinContent(col + 1, row + 1)
                if (ChipNo, col, row) not in DeadPixelList:
                    self.ResultData['Plot']['ROOTObject'].Fill(col, row, threshold)


        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz') 

        self.ResultData['Plot']['Caption'] = 'Vcal Threshold Trimmed Map'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()