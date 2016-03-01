import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_bareBBMap_TestResult'
        self.NameSingle='bareBBMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Bare BBMap'


    def PopulateResultData(self):

        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(0);

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", 8*self.nCols, 0., 8*self.nCols, 2*self.nRows, 0., 2*self.nRows); # mThreshold

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            try:
                ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
                histo = ChipTestResultObject.ResultData['SubTestResults']['BareBBMap'].ResultData['Plot']['ROOTObject']
                print 'histo name inside BareBBSumary: ', histo.GetName()
                if not histo:
                    print 'cannot get BareBBMap histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                    continue
                print '---------------------',ChipTestResultObject.Attributes['ChipNo']
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
                        self.ResultData['Plot']['ROOTObject'].SetBinContent(tmpCol, tmpRow, histo.GetBinContent(col + 1, row + 1))
                    
            except:
                'No histogram for chip i',i


        if self.ResultData['Plot']['ROOTObject']:

            #self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(mThresholdMin,mThresholdMax);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0.,2.);
            #self.ResultData['Plot']['ROOTObject'].GetYaxis().SetLinY();
            #self.ResultData['Plot']['ROOTObject'].GetXaxis().SetLinX();
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

        self.ResultData['Plot']['Caption'] = 'bare BBmap'
        self.SaveCanvas()        
