# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_HitMap_TestResult'
        self.NameSingle = 'HitMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'NHits': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'NHits'
            },
            'RealHitrate':{
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Real Hitrate',
                'Unit':'MHz/cm2'
            },
            'NumberOfDefectivePixels':{
                'Value':'{Rate}'.format(Rate=-1),
                'Label':'# Defective Pixels'
            }
        }
        self.ResultData['KeyList'] += ['RealHitrate','NumberOfDefectivePixels']
        self.ResultData['HiddenData']['ListOfDefectivePixels'] = []

    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=self.Attributes['Rate'])]
        histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'HitMap').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        NumberOfDefectivePixels = 0
        NumberOfHits = 0
        if self.ResultData['Plot']['ROOTObject']:
            for Row in range(self.nRows):
                for Column in range(self.nCols):
                    PixelHits = self.ResultData['Plot']['ROOTObject'].GetBinContent(Column+1, Row+1)
                    if PixelHits > 0:
                        NumberOfHits += PixelHits
                    else:
                        NumberOfDefectivePixels += 1
                        self.ResultData['HiddenData']['ListOfDefectivePixels'].append((ChipNo, Column, Row))

            self.ResultData['KeyValueDictPairs']['NHits']['Value'] = '{NHits:1.0f}'.format(NHits=NumberOfHits)

            NTriggersROOTObject = (
            HistoGetter.get_histo(
                    self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=self.Attributes['Rate'])],
                    "Xray.ntrig_Ag_V0" 
                )
            )
            TimeConstant = float(self.TestResultEnvironmentObject.XRayHRQualificationConfiguration['TimeConstant'])
            Area = float(self.TestResultEnvironmentObject.XRayHRQualificationConfiguration['Area'])
            NTriggers = float(NTriggersROOTObject.GetBinContent(1))
            NHits = float(self.ResultData['KeyValueDictPairs']['NHits']['Value'])
            RealHitrate = NHits / (NTriggers*TimeConstant*Area)*1e-6

            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()
        self.ResultData['KeyValueDictPairs']['NumberOfDefectivePixels']['Value'] = '{NumberOfDefectivePixels:1.0f}'.format(NumberOfDefectivePixels=NumberOfDefectivePixels)
        self.ResultData['KeyValueDictPairs']['RealHitrate']['Value'] = '{RealHitrate:1.2f}'.format(RealHitrate=RealHitrate)
        self.ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue'] = RealHitrate

        self.Title = 'Hit Map {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])


