import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_VcalThreshold_TestResult'
        self.NameSingle='VcalThreshold'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Vcal Threshold'


    def PopulateResultData(self):


        ROOT.gStyle.SetOptStat(0);
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", 8*self.nCols, 0., 8*self.nCols, 2*self.nRows, 0., 2*self.nRows); # mThreshold

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['VcalThresholdUntrimmed'].ResultData['Plot']['ROOTObject']
            print histo
            if not histo:
                print 'cannot get VcalThresholdUntrimmed histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
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

                    self.ResultData['Plot']['ROOTObject'].SetBinContent(tmpCol, tmpRow, histo.GetBinContent(j+1, k+1))



        if self.ResultData['Plot']['ROOTObject']:
            mThresholdMin = 0.
            mThresholdMax = 255.

            if  self.ResultData['Plot']['ROOTObject'].GetMaximum() < mThresholdMax:
                mThresholdMax = self.ResultData['Plot']['ROOTObject'].GetMaximum();

            if self.ResultData['Plot']['ROOTObject'].GetMinimum() > mThresholdMin:
                mThresholdMin = self.ResultData['Plot']['ROOTObject'].GetMinimum();


            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(mThresholdMin,mThresholdMax);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');


        box = ROOT.TBox();
        box.SetFillColor(3);
        box.SetFillStyle(3004);
        if self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 0:
            box.SetFillColor(29);
            box.DrawBox( 0, 0,  8*self.nCols,  self.nRows);
        elif self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 8:
            box.SetFillColor(29);
            box.DrawBox( 0, 0,  8*self.nCols,  2*self.nRows);

        self.ResultData['Plot']['Format'] = 'png'

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['Caption'] = 'Vcal Threshold'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
