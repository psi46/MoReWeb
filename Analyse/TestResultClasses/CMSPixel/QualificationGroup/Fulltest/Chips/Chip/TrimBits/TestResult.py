# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TrimBits_TestResult'
        self.NameSingle='TrimBits'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        

        
    def PopulateResultData(self):
        
        ROOT.gStyle.SetOptStat(0);
        #self.ResultData['Plot']['ROOTObject'] =  ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows ) # htm
        # TH2D
        
        ChipNo=self.ParentObject.Attributes['ChipNo']
        histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle,'TrimBits')%ChipNo
        self.ResultData['Plot']['ROOTObject'] =  self.ParentObject.ParentObject.FileHandle.Get(histname).Clone(self.GetUniqueID())
        mean = 0
        rms  = 0

        if self.ResultData['Plot']['ROOTObject']:
            #for i in range(self.nCols): # Columns
            #    for j in range(self.nRows): # Rows
            #        self.ResultData['Plot']['ROOTObject'].SetBinContent(i+1, j+1, self.ResultData['Plot']['ROOTObject_TrimMap'].GetBinContent(i+1, j+1))
            
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            self.ResultData['Plot']['ROOTObject'].SetFillStyle(3002)
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlack)
            #self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0., self.nTotalChips);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Trim bits");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("entries");
#            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
#            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('');
            mean  = self.ResultData['Plot']['ROOTObject'].GetMean() 
            rms   = self.ResultData['Plot']['ROOTObject'].GetRMS()
        self.ResultData['KeyValueDictPairs'] = { 
            'mu': {
                'Value':'{0:1.2f}'.format(mean), 
                'Label':'μ'
            },  
            'sigma':{
                'Value':'{0:1.2f}'.format(rms), 
                'Label':'σ'
            }   
        }   
        self.ResultData['KeyList'] = ['mu','sigma']
            

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Trim Bits'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
