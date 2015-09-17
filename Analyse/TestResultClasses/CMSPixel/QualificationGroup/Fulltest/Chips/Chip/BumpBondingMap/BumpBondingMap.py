# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle = 'BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.Attributes['isDigitalROC'] = self.ParentObject.ParentObject.ParentObject.Attributes['isDigital']

    def PopulateResultData(self):
        # initialize ROOT
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

        # initialize data
        isDigital = self.Attributes['isDigitalROC']
        if isDigital:
            thr = self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Threshold']['Value']
        deadBumps = self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['DeadBumps']
        histo = self.ParentObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject']
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows)

        # fill plot
        for col in range(self.nCols):
            for row in range(self.nRows):
                result = histo.GetBinContent(col + 1, row + 1)
                if isDigital:
                    result = not (result < thr)
                self.ResultData['Plot']['ROOTObject'].SetBinContent(col + 1, row + 1, result)

        # draw
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            if isDigital:
                self.ResultData['Plot']['ROOTObject'].Draw('colz')
                self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, 1)
            else:
                self.ResultData['Plot']['ROOTObject'].SetMaximum(2.)
                self.ResultData['Plot']['ROOTObject'].SetMinimum(-2.)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        # save
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()

