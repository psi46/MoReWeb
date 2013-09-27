# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBonding_TestResult'
        self.NameSingle='BumpBonding'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        

        
        ROOT.gPad.SetLogy(1);
        isDigitalROC = self.ParentObject.ParentObject.ParentObject.Attributes['isDigital']
        mean = -9999
        rms = -9999
        nBumpBondingProblems = 0;
        nSigma = self.TestResultEnvironmentObject.GradingParameters['BumpBondingProblemsNSigma']
        thr=0
        # TH1D
        try:
            self.ResultData['Plot']['ROOTObject'] =   self.ParentObject.ParentObject.FileHandle.Get("vcals_xtalk_C{ChipNo}Distribution".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())
        except:
            pass
        if not self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'] = self.ParentObject.ParentObject.FileHandle.Get("BumpBondMap_C{ChipNo}Distribution".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            if not isDigitalROC:
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0*self.ResultData['Plot']['ROOTObject'].GetMaximum());
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Threshold difference");  
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();
            mean =   self.ResultData['Plot']['ROOTObject'].GetMean()
            rms =   self.ResultData['Plot']['ROOTObject'].GetRMS()
            thr = mean + nSigma * rms
            startbin = self.ResultData['Plot']['ROOTObject'].FindBin(thr)
            for bin in range(startbin,self.ResultData['Plot']['ROOTObject'].GetNbinsX()):
                nBumpBondingProblems += self.ResultData['Plot']['ROOTObject'].GetBinContent(bin)
            self.Cut = ROOT.TCutG('bumpBondingThreshold',2)
            self.Cut.SetPoint(0,thr,-1e9)
            self.Cut.SetPoint(1,thr,+1e9)
            self.Cut.SetLineWidth(2)
            self.Cut.SetLineStyle(2)
            self.Cut.SetLineColor(ROOT.kRed)
            self.Cut.Draw()
        
        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
        self.ResultData['KeyValueDictPairs']['Mean'] = {'Value':round(mean,2), 'Label':'Mean',}
        self.ResultData['KeyList'].append('Mean')
        self.ResultData['KeyValueDictPairs']['RMS'] = {'Value':round(rms,2), 'Label':'RMS',}
        self.ResultData['KeyList'].append('RMS')
        
        if isDigitalROC:
                self.ResultData['KeyValueDictPairs']['nSigma'] = {'Value':  nSigma, 'Label':'σ'}
                self.ResultData['KeyValueDictPairs']['Threshold'] = {'Value':  round(thr,2), 'Label':'threshold'}
                self.ResultData['KeyValueDictPairs']['nBumpBondingProblems'] = {'Value': round(nBumpBondingProblems,0), 'Label':'N BumpProblems'}
                self.ResultData['KeyList'].append('nSigma')
                self.ResultData['KeyList'].append('Threshold')
                self.ResultData['KeyList'].append('nBumpBondingProblems')
                
        
