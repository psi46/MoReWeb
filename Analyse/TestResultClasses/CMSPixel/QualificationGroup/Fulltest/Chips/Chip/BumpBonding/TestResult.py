import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBonding_TestResult'
        self.NameSingle='BumpBonding'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        

        
        ROOT.gPad.SetLogy(1);
        
        # TH1D
        self.ResultData['Plot']['ROOTObject'] =   self.ParentObject.ParentObject.FileHandle.Get("vcals_xtalk_C{ChipNo}Distribution".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())
        
        
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0*self.ResultData['Plot']['ROOTObject'].GetMaximum());
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Threshold difference");  
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();


        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
