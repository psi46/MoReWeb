import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'CalDelVthrcomp'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_OnShellQuickTest_ROC'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        HistoName = HistoDict.get('OnShellQuickTest', 'CalDelVthrcomp')
        ChipNo = self.ParentObject.Attributes['ChipNo']
        ROOTFile = self.ParentObject.ParentObject.FileHandle

        try:
            self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(ROOTFile, HistoName, rocNo=ChipNo).Clone(self.GetUniqueID())
        except:
            self.ResultData['Plot']['ROOTObject'] = None

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].Draw("colz")

        self.Title = 'CalDel/Vthrcomp'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()