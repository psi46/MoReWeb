# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_VcalThresholdTrimmed_TestResult'
        self.NameSingle='VcalThresholdTrimmed'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        

        
    def PopulateResultData(self):
        
        
        
        ROOT.gPad.SetLogy(1);
        ROOT.gStyle.SetOptStat(1);
        
        # TH1D
        self.ResultData['Plot']['ROOTObject'] =   self.ParentObject.ParentObject.FileHandle.Get("VcalThresholdMap_C{ChipNo}Distribution;7".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())
        
        
        #mG
        MeanVcalThr = self.ResultData['Plot']['ROOTObject'].GetMean()
        #sG
        RMSVcalThr = self.ResultData['Plot']['ROOTObject'].GetRMS()
        #nG
        IntegralVcalThr = self.ResultData['Plot']['ROOTObject'].Integral(
            self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(), 
            self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
        )
        #nG_entries
        IntegralVcalThr_Entries = self.ResultData['Plot']['ROOTObject'].GetEntries()
        
        under = self.ResultData['Plot']['ROOTObject'].GetBinContent(0)
        over = self.ResultData['Plot']['ROOTObject'].GetBinContent(self.ResultData['Plot']['ROOTObject'].GetNbinsX()+1)
                
            
        self.ResultData['KeyValueDictPairs'] = {
            'N': {
                'Value':'{0:1.0f}'.format(IntegralVcalThr), 
                'Label':'N'
            },
            'mu': {
                'Value':'{0:1.2f}'.format(MeanVcalThr), 
                'Label':'μ'
            },
            'sigma':{
                'Value':'{0:1.2f}'.format(RMSVcalThr), 
                'Label':'σ'
            }
        }
        self.ResultData['KeyList'] = ['N','mu','sigma']
        if under:
            self.ResultData['KeyValueDictPairs']['under'] = {'Value':'{0:1.2f}'.format(under), 'Label':'<='}
            self.ResultData['KeyList'].append('under')
        if over:
            self.ResultData['KeyValueDictPairs']['over'] = {'Value':'{0:1.2f}'.format(over), 'Label':'>='}
            self.ResultData['KeyList'].append('over')
    
        
        
        
        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            self.ResultData['Plot']['ROOTObject'].SetAxisRange(0, 100);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Vcal Threshold");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();
            
            
                

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Vcal Threshold Trimmed'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
