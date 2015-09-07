import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_HotPixelSummary_TestResult'
        self.NameSingle='HotPixelSummary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        RocNumbers = array.array('d')
        HotPixels = array.array('d')

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            MissingHits = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfHotPixels_{Rate}'.format(Rate=self.Attributes['Rate'])]['Value']
            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            RocNumbers.append(ChipNo)
            HotPixels.append(MissingHits)
             
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(RocNumbers), RocNumbers, HotPixels)

        if self.ResultData['Plot']['ROOTObject']:
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("ROC")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kOrange+7)
            self.ResultData['Plot']['ROOTObject'].SetMarkerColor(ROOT.kOrange+7)
            self.ResultData['Plot']['ROOTObject'].SetMarkerStyle(ROOT.kFullSquare)
            self.ResultData['Plot']['ROOTObject'].Draw('APL')

        self.Title = 'Hot pixels {Rate}'.format(Rate=self.Attributes['Rate'])
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()