import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='TrimBitMap'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        # initialize data
        xBins = 8 * self.nCols
        yBins = 2 * self.nRows
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins);  # mBumps

        # fill plot
        SpecialBumpBondingTestNamesROC = []
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['TrimBitMap'].ResultData['Plot']['ROOTObject']

            if not histo:
                print 'cannot get TrimBitMap histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            for col in range(self.nCols):
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.UpdatePlot(chipNo, col, row, result)

        # draw
        if self.ResultData['Plot']['ROOTObject']:
            try:
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTickLength(0.015)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTickLength(0.012)
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetAxisColor(1, 0.4)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetAxisColor(1, 0.4)
                self.Canvas.SetFrameLineStyle(0)
                self.Canvas.SetFrameLineWidth(1)
                self.Canvas.SetFrameBorderMode(0)
                self.Canvas.SetFrameBorderSize(1)
                self.Canvas.SetCanvasSize(1500, 376)
            except:
                pass
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')


        boxes = []
        startChip = self.ParentObject.Attributes['StartChip']
        endChip = self.ParentObject.Attributes['NumberOfChips'] + startChip - 1
        if self.verbose:
            print 'Used chips: %2d -%2d' % (startChip, endChip)
        for i in range(0,16):
            if i < startChip or endChip < i:
                if i < 8:
                    j = 15 - i
                else:
                    j = i - 8
                beginX = (j % 8) * self.nCols
                endX = beginX + self.nCols
                beginY = int(j / 8) * self.nRows
                endY = beginY + self.nRows
                if self.verbose:
                    print 'chip %d not used.' % i, j, '%d-%d , %d-%d' % (beginX, endX, beginY, endY)
                newBox = ROOT.TPaveText(beginX, beginY, endX, endY)
                newBox.SetFillColor(29)
                newBox.SetLineColor(29)
                newBox.SetFillStyle(3004)
                newBox.SetShadowColor(0)
                newBox.SetBorderSize(1)
                newBox.Draw()
                boxes.append(newBox)

        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Trim Bit Map'
        self.SaveCanvas()

    def UpdatePlot(self, chipNo, col, row, value):
        result = value
        if chipNo < 8:
            tmpCol = 8 * self.nCols - 1 - chipNo * self.nCols - col
            tmpRow = 2 * self.nRows - 1 - row
        else:
            tmpCol = (chipNo % 8 * self.nCols + col)
            tmpRow = row
        # Get the data from the chip sub test result bump bonding

        if result and self.verbose:
            print chipNo, col, row, '--->', tmpCol, tmpRow, result
#         self.ResultData['Plot']['ROOTObject'].SetBinContent(tmpCol + 1, tmpRow + 1, result)
        self.ResultData['Plot']['ROOTObject'].Fill(tmpCol, tmpRow, result)
