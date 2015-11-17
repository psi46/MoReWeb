import ROOT
import AbstractClasses
import os
from operator import itemgetter
import warnings
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.NameSingle = 'ReadbackCalVana'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        HistoName = HistoDict.get(self.NameSingle, 'VanaCalibration')
        #HistoName = 'Readback.rbVa_C%d_V0'
        print HistoName
        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        try:
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(ROOTFile, HistoName, rocNo=ChipNo).Clone(self.GetUniqueID())
        except:
            pass

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle('');
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitleOffset(1.3);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.8);
            self.ResultData['Plot']['ROOTObject'].Draw()

        self.Title = 'Vana [ADC]/Vana [V]'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.SaveCanvas()