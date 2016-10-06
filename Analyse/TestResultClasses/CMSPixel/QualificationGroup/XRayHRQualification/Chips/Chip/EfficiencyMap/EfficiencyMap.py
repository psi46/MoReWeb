# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_EfficiencyMap_TestResult'
        self.NameSingle = 'EfficiencyMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        #self.ResultData['Plot']['Format'] = 'png'
        #self.AdditionalImageFormats = ['root']
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HREfficiency_{Rate}'.format(Rate=self.Attributes['Rate'])]
        try:
            histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'EfficiencyMap').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())
        except: 
            histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate2', 'EfficiencyMap').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())
        self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            #self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.);
            #self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0 * self.ResultData['Plot'][
            #    'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');
            

        self.Title = 'Efficiency Map {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()        


