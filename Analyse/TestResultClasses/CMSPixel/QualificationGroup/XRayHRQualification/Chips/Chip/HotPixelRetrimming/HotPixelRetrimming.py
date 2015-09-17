# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_HotPixelRetrimming_TestResult'
        self.NameSingle = 'HotPixelRetrimming'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.RetrimmedHotPixelsList = set()
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        ROOT.gPad.SetLogx(0)
        ROOT.gStyle.SetOptStat(0)
        self.Canvas.Clear()
        self.ResultData['Plot']['ROOTObject'] = None

        if 'RetrimHotPixels' in self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']:
            rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['RetrimHotPixels']
            histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'RetrimHotPixels').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())
        else:
            self.DisplayOptions['Show'] = False
            self.ResultData['Plot']['ROOTObject'] = None
            self.ResultData['KeyList'] = []

        if self.ResultData['Plot']['ROOTObject']:
            for col in range(0, self.nCols):
                for row in range(0, self.nRows):
                    if self.ResultData['Plot']['ROOTObject'].GetBinContent(1+col,1+row) > 0:
                        self.RetrimmedHotPixelsList.add((ChipNo, col, row))

            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

        self.ResultData['HiddenData']['ListOfRetrimmedHotPixels'] = {'Label': 'Retrimmed Hot Pixels List', 'Value': self.RetrimmedHotPixelsList}
        self.ResultData['HiddenData']['NumberOfRetrimmedHotPixels'] = {'Label': 'Retrimmed Hot Pixels', 'Value': len(self.RetrimmedHotPixelsList)}

        self.Title = 'Retrim Hot Pix {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()        


