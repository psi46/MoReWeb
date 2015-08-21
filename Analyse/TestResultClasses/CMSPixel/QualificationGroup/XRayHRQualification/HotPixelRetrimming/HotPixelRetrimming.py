# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='HotPixelRetrimming'
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins)
        DisplayOptionsShow = True

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            chipNo = ChipTestResultObject.Attributes['ChipNo']

            if histo:
                for col in range(self.nCols): 
                    for row in range(self.nRows):
                        result = histo.GetBinContent(col + 1, row + 1)
                        self.UpdatePlot(chipNo, col, row, result)
            DisplayOptionsShow = DisplayOptionsShow and (ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].DisplayOptions['Show'] if ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].DisplayOptions.has_key('Show') else True)

        self.DisplayOptions['Show'] = DisplayOptionsShow

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("Δ trimbit")
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitleOffset(0.5)
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        self.Title = 'Retrimmed Hot Pixels {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()     

    def UpdatePlot(self, chipNo, col, row, value):
        result = value
        if chipNo < 8:
            tmpCol = 8 * self.nCols - 1 - chipNo * self.nCols - col
            tmpRow = 2 * self.nRows - 1 - row
        else:
            tmpCol = (chipNo % 8 * self.nCols + col)
            tmpRow = row
        # Get the data from the chip sub test result hitmap

        if result and self.verbose:
            print chipNo, col, row, '--->', tmpCol, tmpRow, result
        self.ResultData['Plot']['ROOTObject'].Fill(tmpCol, tmpRow, result)
