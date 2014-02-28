import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TrimBitTest_TestResult'
        self.NameSingle='TrimBitTest'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        

        
    def PopulateResultData(self):
        

        
        ROOT.gPad.SetLogy(1);
        
        # TH1D
        fileHandle = self.ParentObject.ParentObject.FileHandle
        ChipNo=self.ParentObject.Attributes['ChipNo']
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        histname = HistoDict.get(self.NameSingle,'TrimBit0')%ChipNo
        self.ResultData['Plot']['ROOTObject'] = fileHandle.Get(histname).Clone(self.GetUniqueID())
        
        # TH1D
        histname = HistoDict.get(self.NameSingle,'TrimBit1')%ChipNo
        self.ResultData['Plot']['ROOTObject_TrimBit13'] = fileHandle.Get(histname).Clone(self.GetUniqueID())
        # TH1D
        histname = HistoDict.get(self.NameSingle,'TrimBit2')%ChipNo
        self.ResultData['Plot']['ROOTObject_TrimBit11'] = fileHandle.Get(histname).Clone(self.GetUniqueID())
        # TH1D
        histname = HistoDict.get(self.NameSingle,'TrimBit3')%ChipNo
        self.ResultData['Plot']['ROOTObject_TrimBit7'] = fileHandle.Get(histname).Clone(self.GetUniqueID())
        
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            self.ResultData['Plot']['ROOTObject'].SetAxisRange(0., 60.);
            self.ResultData['Plot']['ROOTObject'].SetMinimum(0.5);
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlack);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Threshold difference");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            
            self.ResultData['Plot']['ROOTObject'].Draw();
            
            self.ResultData['Plot']['ROOTObject_TrimBit13'].SetLineColor(ROOT.kRed);
            self.ResultData['Plot']['ROOTObject_TrimBit13'].Draw('same');
            
            
            self.ResultData['Plot']['ROOTObject_TrimBit11'].SetLineColor(ROOT.kBlue);
            self.ResultData['Plot']['ROOTObject_TrimBit11'].Draw('same');
            
            
            self.ResultData['Plot']['ROOTObject_TrimBit7'].SetLineColor(ROOT.kGreen);
            self.ResultData['Plot']['ROOTObject_TrimBit7'].Draw('same');
            
            Legend = ROOT.TLegend()
            Legend.AddEntry(self.ResultData['Plot']['ROOTObject'], 'Trim Value 14', 'l')
            Legend.AddEntry(self.ResultData['Plot']['ROOTObject_TrimBit13'], 'Trim Value 13', 'l')
            Legend.AddEntry(self.ResultData['Plot']['ROOTObject_TrimBit11'], 'Trim Value 11', 'l')
            Legend.AddEntry(self.ResultData['Plot']['ROOTObject_TrimBit7'], 'Trim Value 7', 'l')
            Legend.Draw()
            

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Trim Bit Test'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
