import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='PHMap'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

        # TH2D
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        ChipNo = self.ParentObject.Attributes['ChipNo']

        if self.HistoDict.has_option(self.NameSingle, self.Attributes['Map']):
            histname = self.HistoDict.get(self.NameSingle, self.Attributes['Map'])
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            self.ResultData['Plot']['ROOTObject'] = object.Clone(self.GetUniqueID())

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw("colz")

        self.Title = 'PH Map: %s'%(self.Attributes['Map'] if 'Map' in self.Attributes else '?')
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)

        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()
