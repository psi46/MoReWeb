# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import math

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_CalDelScan_TestResult'
        self.NameSingle = 'CalDelScan'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {}
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'CalDelScan').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        histogramName2 = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate2', 'CalDelScan').format(ChipNo=self.ParentObject.Attributes['ChipNo'])

        self.Canvas.Clear()
        
        if 'CalDelScan' in self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']:
            rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['CalDelScan']
            try:
                self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())
            except:
                self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName2).Clone(self.GetUniqueID())

            if self.ResultData['Plot']['ROOTObject']:
                ROOT.gStyle.SetOptStat(0)
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("CalDel")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Efficiency")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw()

        self.Title = 'CalDel scan: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        


