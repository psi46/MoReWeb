import ROOT
import AbstractClasses
import ROOT
import math
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_VcalThreshold_TestResult'
        self.NameSingle='VcalThreshold'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Vcal Threshold'


    def PopulateResultData(self):


        ROOT.gStyle.SetOptStat(0);
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", 8*self.nCols, 0., 8*self.nCols, 2*self.nRows, 0., 2*self.nRows); # mThreshold
        ValueList = []
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['VcalThresholdUntrimmed'].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get VcalThresholdUntrimmed histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            # ValueList = []
            
            for col in range(self.nCols): # Columns
                for row in range(self.nRows): # Rows
                    if ChipTestResultObject.Attributes['ChipNo'] < 8:
                        tmpCol = 8*self.nCols-(ChipTestResultObject.Attributes['ChipNo']*self.nCols+col)
                        tmpRow = 2*self.nRows-row
                    else:
                        tmpCol = (ChipTestResultObject.Attributes['ChipNo']%8*self.nCols+col)+1
                        tmpRow = row+1
                    if ChipTestResultObject.Attributes['ChipNo'] < 8:
                        #tmpRow += self.nRows
                        pass
                    # Get the data from the chip sub test result VcalThresholdUntrimmed
                    Value = histo.GetBinContent(col + 1, row + 1)
                    ValueList.append(Value)
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(tmpCol, tmpRow, Value)



        if self.ResultData['Plot']['ROOTObject']:
            mThresholdMin = 0.
            mThresholdMax = 255.

            if  self.ResultData['Plot']['ROOTObject'].GetMaximum() < mThresholdMax:
                mThresholdMax = self.ResultData['Plot']['ROOTObject'].GetMaximum()

            if self.ResultData['Plot']['ROOTObject'].GetMinimum() > mThresholdMin:
                mThresholdMin = self.ResultData['Plot']['ROOTObject'].GetMinimum()
            if len(ValueList) > 0:
                SortedValueList = sorted(ValueList)
                LowerIndex = int(math.floor(len(SortedValueList)*0.05))
                UpperIndex = int(math.floor(len(SortedValueList)*0.95))
                LowerValueList = SortedValueList[0:LowerIndex-1]
                UpperValueList = SortedValueList[UpperIndex:]
                if SortedValueList[LowerIndex] > 5.*sum(LowerValueList)/float(len(LowerValueList)):
                    mThresholdMin = SortedValueList[LowerIndex]*0.1
                if SortedValueList[UpperIndex]*5. < sum(UpperValueList)/float(len(UpperValueList)):
                    mThresholdMax = SortedValueList[UpperIndex]*1.1

            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(mThresholdMin,mThresholdMax);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');


        boxes = []
        startChip = self.ParentObject.Attributes['StartChip']
        endChip = self.ParentObject.Attributes['NumberOfChips'] + startChip - 1
        if self.verbose:
            print 'Used chips: %2d -%2d' % (startChip, endChip)
        for i in range(0, 16):
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

        self.ResultData['Plot']['Format'] = 'png'

        self.SaveCanvas()
        self.ResultData['Plot']['Caption'] = 'Vcal Threshold'
        