# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_EfficiencyMap_TestResult'
        self.NameSingle = 'EfficiencyMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
       
    
    def PopulateResultData(self):
        NumberOfLowEfficiencyPixels = 0;
        ChipNo = self.ParentObject.Attributes['ChipNo']
        self.ResultData['Plot']['ROOTObject'] = (
            self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HREfficiency_{:d}'.format(self.Attributes['Rate'])]
            .Get("Xray.highRate_calmap_C{ChipNo}_V0".format(ChipNo=self.ParentObject.Attributes['ChipNo']) )
            .Clone(self.GetUniqueID())
        )
        
        if self.ResultData['Plot']['ROOTObject']:
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
            self.ResultData['Plot']['ROOTObject'].Draw();
            

        self.SaveCanvas()
        self.Title = 'Bump Bonding: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        


