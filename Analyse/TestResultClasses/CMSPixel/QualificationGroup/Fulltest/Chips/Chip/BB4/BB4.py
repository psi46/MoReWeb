# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BB4_TestResult'
        self.NameSingle = 'BB4'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.DeadBumpList = set()

    def PopulateResultData(self):
        # initialize ROOT
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

        # initialize data
        ChipNo = self.ParentObject.Attributes['ChipNo']

        try:
            self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
            histname = self.HistoDict.get(self.NameSingle, "PixelHit")
            histo = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows)

            # if BB4 test exists
            if histo:

                # fill plot
                self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows)
                for col in range(self.nCols):
                    for row in range(self.nRows):
                        value = 1 if histo.GetBinContent(col + 1, row + 1) < 1 else 0
                        if value > 0:
                            self.DeadBumpList.add((ChipNo, col, row))
                        self.ResultData['Plot']['ROOTObject'].SetBinContent(col + 1, row + 1, value)
                # draw
                if self.ResultData['Plot']['ROOTObject']:
                    self.ResultData['Plot']['ROOTObject'].SetTitle("")
                    self.ResultData['Plot']['ROOTObject'].Draw('colz')
                    self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, 1)
                    self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
                    self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                    self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                    self.ResultData['Plot']['ROOTObject'].Draw('colz')

                self.SaveCanvas()

                self.ResultData['KeyValueDictPairs']['DeadBumps'] = {'Value': self.DeadBumpList, 'Label': 'Dead Bumps'}
                self.ResultData['KeyValueDictPairs']['NDeadBumps'] = {'Value': len(self.DeadBumpList), 'Label': 'Dead Bumps'}
                self.ResultData['KeyList'] = ['NDeadBumps']
            else:
                self.DisplayOptions['Show'] = False
                self.ResultData['Plot']['ROOTObject'] = None
                self.ResultData['KeyList'] = []

        except:
            self.DisplayOptions['Show'] = False
            self.ResultData['Plot']['ROOTObject'] = None
            self.ResultData['KeyList'] = []
            pass



        # save

