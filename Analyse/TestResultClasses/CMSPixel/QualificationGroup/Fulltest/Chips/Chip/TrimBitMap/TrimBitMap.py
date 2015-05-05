import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TrimBitMap_TestResult'
        self.NameSingle = 'TrimBitMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

    def PopulateResultData(self):

        ROOT.gStyle.SetOptStat(0)
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols,
                                                          self.nRows, 0., self.nRows)  # htm
        # TH2D

        ChipNo = self.ParentObject.Attributes['ChipNo']
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        histname = HistoDict.get(self.NameSingle, 'TrimBitMap')
        self.ResultData['Plot']['ROOTObject_TrimMap'] = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle,
                                                                              histname,
                                                                              rocNo=ChipNo).Clone(self.GetUniqueID())

        if self.ResultData['Plot']['ROOTObject']:
            for i in range(self.nCols):  # Columns
                for j in range(self.nRows):  # Rows
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(i + 1, j + 1, self.ResultData['Plot'][
                        'ROOTObject_TrimMap'].GetBinContent(i + 1, j + 1))
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0., self.nTotalChips)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Trim bit Map")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("entries")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        self.SaveCanvas()
        self.Title = 'Trim Bit Map'
        