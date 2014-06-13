# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBonding_TestResult'
        self.NameSingle='BumpBonding'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'



    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        ROOT.gPad.SetLogy(1);
        isDigitalROC = self.ParentObject.ParentObject.ParentObject.Attributes['isDigital']
        mean = -9999
        rms = -9999
        nBumpBondingProblems = 0;
        nSigma = self.TestResultEnvironmentObject.GradingParameters['BumpBondingProblemsNSigma']
        thr=0
        # TH1D
        ChipNo=self.ParentObject.Attributes['ChipNo']
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        self.FileHandle = self.ParentObject.ParentObject.FileHandle
        try:
            histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'Analog')
            object =  HistoGetter.get_histo(self.FileHandle,histname,rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
        except:
            histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'Digital')
            object =  HistoGetter.get_histo(self.FileHandle,histname,rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject']  = object.Clone(self.GetUniqueID())
        if self.ResultData['Plot']['ROOTObject']:
            self.Canvas.Clear()
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
            self.Cut.Draw('PL')

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
        self.ResultData['KeyValueDictPairs']['Mean'] = {'Value':round(mean,2), 'Label':'Mean',}
        self.ResultData['KeyList'].append('Mean')
        self.ResultData['KeyValueDictPairs']['RMS'] = {'Value':round(rms,2), 'Label':'RMS',}
        self.ResultData['KeyList'].append('RMS')
        self.ResultData['KeyValueDictPairs']['Threshold'] = {'Value':round(thr,2), 'Label':'Threshold',}
        self.ResultData['KeyList'].append('Threshold')

        if isDigitalROC:
                self.ResultData['KeyValueDictPairs']['nSigma'] = {'Value':  nSigma, 'Label':'σ'}
                self.ResultData['KeyValueDictPairs']['nBumpBondingProblems'] = {'Value': round(nBumpBondingProblems,0), 'Label':'N BumpProblems'}
                self.ResultData['KeyList'].append('nSigma')
                self.ResultData['KeyList'].append('nBumpBondingProblems')


