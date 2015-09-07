# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_BumpBondingDefects_TestResult'
        self.NameSingle = 'BumpBondingDefects'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'NumberOfDefectivePixels': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Bump Bonding Defects'
            },
        }
        self.BBDefectsList = set()

    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=self.Attributes['Rate'])]
        histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'HitMap').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        histoHitMap = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        histoAlive = self.ParentObject.ResultData['SubTestResults']['AliveMap'].ResultData['Plot']['ROOTObject']
        histoHot = self.ParentObject.ResultData['SubTestResults']['HotPixelMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows) 

        try:
            NtrigAlive = self.ParentObject.ParentObject.ParentObject.Attributes['Ntrig']['PixelAlive']
        except:
            NtrigAlive = 10

        if histoHitMap:
            for Row in range(self.nRows):
                for Column in range(self.nCols):
                    PixelHits = histoHitMap.GetBinContent(Column+1, Row+1)
                    PixelAlive = (not histoAlive) or (histoAlive.GetBinContent(Column+1, Row+1) == NtrigAlive)
                    PixelUnmasked = (not histoHot) or (histoHot.GetBinContent(Column+1, Row+1) < 1)

                    if PixelHits < 1 and PixelAlive and PixelUnmasked:
                        self.BBDefectsList.add((ChipNo, Column, Row))
                        self.ResultData['Plot']['ROOTObject'].SetBinContent(Column+1, Row+1, 1)

            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        self.SaveCanvas()
        self.ResultData['KeyValueDictPairs']['NumberOfDefectivePixels']['Value'] = '{NumberOfDefectivePixels:1.0f}'.format(NumberOfDefectivePixels=len(self.BBDefectsList))
        self.ResultData['HiddenData']['ListOfDefectivePixels'] = {'Label': 'BB defects', 'Value': self.BBDefectsList}
        self.Title = 'BB Defects {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        



