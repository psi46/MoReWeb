import ROOT
import AbstractClasses
import os
from operator import itemgetter
import warnings
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


#AdcVsDac: Readback.rbIa_C%d_V0
#CurrentVsDac : Readback.tbIa_C%d_V0

    def CustomInit(self):
        self.NameSingle = 'ReadbackCalIana'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        HistoNameAdcVsDac = HistoDict.get(self.NameSingle, 'AdcVsDac')
        HistoNameCurrentVsDac = HistoDict.get(self.NameSingle, 'CurrentVsDac')

        HistogramAdcVsDac = HistoGetter.get_histo(ROOTFile, HistoNameAdcVsDac, rocNo=ChipNo).Clone(self.GetUniqueID())
        HistogramCurrentVsDac = HistoGetter.get_histo(ROOTFile, HistoNameCurrentVsDac, rocNo=ChipNo).Clone(self.GetUniqueID())

        #self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(numPoints, pointsADC, pointsCurrent)
        self.ResultData['Plot']['ROOTObject'] = None

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].Draw()

        self.Title = 'Vdig [ADC]/Vd [V]'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.SaveCanvas()