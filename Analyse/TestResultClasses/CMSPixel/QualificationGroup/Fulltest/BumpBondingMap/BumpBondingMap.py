import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle='BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'



    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0);
        ROOT.gStyle.SetOptStat(0)
        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins);  # mBumps
        isDigital = False
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            isDigital = ChipTestResultObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs'].has_key('Threshold')
            if isDigital:
                thr = ChipTestResultObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Threshold']['Value']
            deadBumps = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['KeyValueDictPairs']['DeadBumps']
            histo = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get BumpBondingProblems histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            for col in range(self.nCols):  # Columns
                for row in range(self.nRows):  # Rows
                    result = histo.GetBinContent(col + 1, row + 1)
                    if isDigital:
                        result = not (result < thr)
                    self.UpdatePlot(chipNo, col, row, result)
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            if isDigital:
                self.ResultData['Plot']['ROOTObject'].Draw('colz');
                self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, 1);
            else:
                self.ResultData['Plot']['ROOTObject'].SetMaximum(2.);
                self.ResultData['Plot']['ROOTObject'].SetMinimum(-2.);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("#Delta Threshold [DAC]");
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');


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
#                 newBox.AddText('%2d' % i)
                newBox.SetFillColor(29)
                newBox.SetLineColor(29)
                newBox.SetFillStyle(3004)
                newBox.SetShadowColor(0)
                newBox.SetBorderSize(1)
                newBox.Draw()
                boxes.append(newBox)
                # (beginX, beginY, endX, endY)
#         if self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 0:
#             box.SetFillColor(29);
#             box.DrawBox( 0, 0,  8*self.nCols,  self.nRows);
#         elif self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 8:
#             box.SetFillColor(29);
#             box.DrawBox(0, self.nRows, 8 * self.nCols, 2 * self.nRows);
#         elif self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 8:
#             box.SetFillColor(29);
#             box.DrawBox( 0, 0,  8*self.nCols,  2*self.nRows);

        self.ResultData['Plot']['Format'] = 'png'

        self.SaveCanvas()
        self.Title = 'Bump Bonding Map'
        
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
