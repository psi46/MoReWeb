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
        ROOT.gStyle.SetOptStat(0);
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(),     "",self.nCols, 0., 8*self.nCols, 2*self.nRows, 0.,2*self.nRows); # mBumps
        
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            isDigital = ChipTestResultObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs'].has_key('Threshold')
            if isDigital:
                thr = ChipTestResultObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Threshold']['Value']
            for j in range(self.nCols): # Columns
                for k in range(self.nRows): # Rows
                    if ChipTestResultObject.Attributes['ChipNo'] < 8:
                        tmpCol = 8*self.nCols-(ChipTestResultObject.Attributes['ChipNo']*self.nCols+j)
                        tmpRow = 2*self.nRows-k
                    else:
                        tmpCol = (ChipTestResultObject.Attributes['ChipNo']%8*self.nCols+j)+1
                        tmpRow = k+1
                    if ChipTestResultObject.Attributes['ChipNo'] < 8:
                        #tmpRow += self.nRows
                        pass
                    # Get the data from the chip sub test result bump bonding
                    result = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject'].GetBinContent(j+1, k+1)
                    if isDigital:
                        result = not (result < thr)
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(tmpCol, tmpRow, result)
                    
        
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            if isDigital:
                self.ResultData['Plot']['ROOTObject'].SetMaximum(1);
                self.ResultData['Plot']['ROOTObject'].SetMinimum(0);
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
        
        
        box = ROOT.TBox();
        box.SetFillColor(3);
        box.SetFillStyle(3004);
        if self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 0: 
            box.SetFillColor(29);
            box.DrawBox( 0, 0,  8*self.nCols,  self.nRows);
        elif self.ParentObject.Attributes['NumberOfChips'] < self.nTotalChips and self.ParentObject.Attributes['StartChip'] == 8:
            box.SetFillColor(29);
            box.DrawBox( 0, 0,  8*self.nCols,  2*self.nRows);
        
        #self.ResultData['Plot']['Format'] = 'png'
        
        
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        #self.Canvas.SaveAs(self.GetPlotFileName()+'.root')
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding Map'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
