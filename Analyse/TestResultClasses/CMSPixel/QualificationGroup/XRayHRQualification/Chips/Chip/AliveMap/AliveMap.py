# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_AliveMap_TestResult'
        self.NameSingle = 'AliveMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        ROOT.gPad.SetLogx(0)
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)
        self.Canvas.Clear()

        if 'PixelAlive' in self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']:
            rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['PixelAlive']
            histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'AliveMap').format(ChipNo=self.ParentObject.Attributes['ChipNo'])

            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

            if self.ResultData['Plot']['ROOTObject']:
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw('colz')
                

        self.Title = 'Alive Map: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        


