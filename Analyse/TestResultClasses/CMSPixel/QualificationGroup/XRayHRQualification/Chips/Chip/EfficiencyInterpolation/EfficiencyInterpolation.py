# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_EfficiencyInterpolation_TestResult'
        self.NameSingle = 'EfficiencyInterpolation'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        if len(Rates)>=2:
            
            
            for Rate in Rates:
                RealHitRate = float(self.ParentObject.ResultData['SubTestResults']['BackgroundMap_{:d}'.format(Rate)].ResultData['KeyValueDictPairs']['RealHitrate']['Value'])
                
        
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            #self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.);
            #self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0 * self.ResultData['Plot'][
            #    'ROOTObject'].GetMaximum())
            #self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Threshold difference");
            #self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            #self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            #self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            #self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');
            

        self.SaveCanvas()
        self.Title = 'Efficiency Interpolation: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        


