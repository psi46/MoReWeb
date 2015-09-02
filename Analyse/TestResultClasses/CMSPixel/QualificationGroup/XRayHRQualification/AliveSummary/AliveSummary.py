import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_AliveSummary_TestResult'
        self.NameSingle='AliveSummary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        RocNumbers = array.array('d')
        DeadPixelList = array.array('d')
        InefficientPixelList = array.array('d')

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            DeadPixels = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfDeadPixels']
            InefficientPixels = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfInefficientPixels']
            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            RocNumbers.append(ChipNo)
            DeadPixelList.append(DeadPixels)
            InefficientPixelList.append(InefficientPixels)
             
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(RocNumbers), RocNumbers, InefficientPixelList)

        if self.ResultData['Plot']['ROOTObject']:
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kOrange+10)
            self.ResultData['Plot']['ROOTObject'].SetMarkerColor(ROOT.kOrange+10)
            self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(ROOT.kFullSquare)
            self.ResultData['Plot']['ROOTObject'].Draw('APL')

        DeadPixelsGraph = ROOT.TGraph(len(RocNumbers), RocNumbers, DeadPixelList)

        if DeadPixelsGraph:
            DeadPixelsGraph.SetTitle("")
            DeadPixelsGraph.GetYaxis().SetTitle("")
            DeadPixelsGraph.GetXaxis().SetTitle("ROC")
            DeadPixelsGraph.GetXaxis().CenterTitle()
            DeadPixelsGraph.SetLineColor(ROOT.kRed+2)
            DeadPixelsGraph.SetMarkerColor(ROOT.kRed+2)
            DeadPixelsGraph.SetMarkerStyle(ROOT.kFullSquare)
            DeadPixelsGraph.Draw('PL,SAME')

        self.Title = 'Dead/inefficient pixels'
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()