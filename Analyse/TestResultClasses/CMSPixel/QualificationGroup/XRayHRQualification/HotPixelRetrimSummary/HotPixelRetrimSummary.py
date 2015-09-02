import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='HotPixelRetrimSummary'
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        RocNumbers = array.array('d')
        HotPixels = array.array('d')

        DisplayOptionsShow = True
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            RetrimmedPixels = ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['HiddenData']['NumberOfRetrimmedHotPixels']['Value']

            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            RocNumbers.append(ChipNo)
            HotPixels.append(RetrimmedPixels)
            DisplayOptionsShow = DisplayOptionsShow and (ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].DisplayOptions['Show'] if ChipTestResultObject.ResultData['SubTestResults']['HotPixelRetrimming_{Rate}'.format(Rate=self.Attributes['Rate'])].DisplayOptions.has_key('Show') else True)

        self.DisplayOptions['Show'] = DisplayOptionsShow
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

        self.Title = 'Retri Hot Pix {Rate}'.format(Rate=self.Attributes['Rate'])
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()