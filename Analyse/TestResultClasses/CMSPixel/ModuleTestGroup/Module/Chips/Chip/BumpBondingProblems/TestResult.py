import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_Chips_Chip_BumpBondingProblems_TestResult'
        self.NameSingle='BumpBondingProblems'
        self.Attributes['TestedObjectType'] = 'CMSPixel_ModuleTestGroup_Module_ROC'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        
        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(0);
        
        # TH2D
        self.ResultData['Plot']['ROOTObject'] =   self.ParentObject.ParentObject.FileHandle.Get("vcals_xtalk_C{ChipNo}".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())
        
        
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(self.TestResultEnvironmentObject.GradingParameters['minThrDiff'], self.TestResultEnvironmentObject.GradingParameters['maxThrDiff']);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("#Delta Threshold [DAC]");
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw("colz");
            self.ResultData['Plot']['ROOTObject'].SaveAs(self.GetPlotFileName()+'.cpp')

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding Problems: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
