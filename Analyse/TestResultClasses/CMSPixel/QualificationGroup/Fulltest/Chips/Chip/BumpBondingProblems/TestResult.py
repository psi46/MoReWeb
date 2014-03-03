import ROOT
import AbstractClasses
from sets import Set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBondingProblems_TestResult'
        self.NameSingle='BumpBondingProblems'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.DeadBumpList = Set()
        self.isDigitalROC =  self.ParentObject.ParentObject.ParentObject.Attributes['isDigital'] 
        self.chipNo=self.ParentObject.Attributes['ChipNo']

        
    def PopulateResultData(self):
        
        ROOT.gStyle.SetOptStat(0);
        ROOT.gPad.SetLogy(0);
        # TH2D
        ChipNo=self.ParentObject.Attributes['ChipNo']
        try:
            histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'Analog')%ChipNo
            self.ResultData['Plot']['ROOTObject'] =   self.ParentObject.ParentObject.FileHandle.Get(histname).Clone(self.GetUniqueID())
        except:
            histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'Digital')%ChipNo
            self.ResultData['Plot']['ROOTObject'] =   self.ParentObject.ParentObject.FileHandle.Get(histname).Clone(self.GetUniqueID())
#             if not isDigitalROC:
#                 print "ERROR Cannot find vcals_xtal_CXXX but is analog Module..."
#             elif isDigitalROC:
#                 print "ERROR: FOound vcals_xtal_CXXX but is digital Module..."
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            if not self.isDigitalROC:
                self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(self.TestResultEnvironmentObject.GradingParameters['minThrDiff'], self.TestResultEnvironmentObject.GradingParameters['maxThrDiff']);
            else:
                self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0,255)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetTitle("#Delta Threshold [DAC]");
            self.ResultData['Plot']['ROOTObject'].GetZaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw("colz");
            self.ResultData['Plot']['ROOTObject'].SaveAs(self.GetPlotFileName()+'.cpp')
        self.CheckBumpBondingProblems()
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding Problems: C{ChipNo}'.format(ChipNo=self.chipNo)
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
    
    def CheckBumpBondingProblems(self):
        BumpBondingProblems_Mean = self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['Mean']['Value']
        BumpBondingProblems_RMS = self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['RMS']['Value']
        BumpBondingProblems_nSigma = 0
        if self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs'].has_key('nSigma'):
            BumpBondingProblems_nSigma = self.ParentObject.ResultData['SubTestResults']['BumpBonding'].ResultData['KeyValueDictPairs']['nSigma']['Value']
        threshold = BumpBondingProblems_Mean+ BumpBondingProblems_nSigma * BumpBondingProblems_RMS
        for column in range(self.nCols):
            for row in range(self.nRows):
                self.HasBumpBondingProblems(column,row,threshold)
        
    def HasBumpBondingProblems(self,column,row,threshold):
        binContent = self.ResultData['Plot']['ROOTObject'].GetBinContent(column+1, row+1)
        if self.isDigitalROC:
            if binContent >= threshold:
                self.DeadBumpList.add((self.chipNo,column,row))
                return True
        else:# is analog ROC    
            if binContent >= self.TestResultEnvironmentObject.GradingParameters['minThrDiff']:#analog Roc
                self.DeadBumpList.add((self.chipNo,column,row))
                return True
        return False
    