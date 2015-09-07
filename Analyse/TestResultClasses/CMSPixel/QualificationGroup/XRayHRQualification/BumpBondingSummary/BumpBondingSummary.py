import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_BumpBondingSummary_TestResult'
        self.NameSingle='BumpBondingSummary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogx(0)
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        RocNumbers = array.array('d')
        BBProblems = array.array('d')

        Maximum = 0
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            BumpBondingDefects = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['BumpBondingDefects_{Rate}'.format(Rate=self.Attributes['Rate'])]['Value']
            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            RocNumbers.append(ChipNo)
            BBProblems.append(BumpBondingDefects)
            if BumpBondingDefects > Maximum:
                Maximum = BumpBondingDefects
             
        self.ResultData['Plot']['ROOTGraph'] = ROOT.TGraph(len(RocNumbers), RocNumbers, BBProblems)

        if self.ResultData['Plot']['ROOTGraph']:
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTGraph'].SetTitle("")
            self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().SetTitle("ROC")
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTGraph'].SetLineColor(ROOT.kBlue)
            self.ResultData['Plot']['ROOTGraph'].SetMarkerColor(ROOT.kBlue)
            self.ResultData['Plot']['ROOTGraph'].SetMarkerStyle(ROOT.kFullSquare)
            if Maximum < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B']*1.1:
                self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetRangeUser(0, self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B']*1.1)

            self.ResultData['Plot']['ROOTGraph'].Draw('APL')

            lineB = ROOT.TLine().DrawLine(
                0, self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B'] - 0.5,
                len(RocNumbers), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_B'] - 0.5,
            )
            lineB.SetLineWidth(2)
            lineB.SetLineStyle(2)
            lineB.SetLineColor(ROOT.kRed)

            if Maximum > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_C']:
                lineC = ROOT.TLine().DrawLine(
                    0, self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_C'] - 0.5,
                    len(RocNumbers), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_missing_xray_pixels_C'] - 0.5,
                )
                lineC.SetLineWidth(2)
                lineC.SetLineStyle(2)
                lineC.SetLineColor(ROOT.kRed)

            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTGraph']

        self.Title = 'BB defects {Rate}'.format(Rate=self.Attributes['Rate'])
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()