import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_NoiseSummary_TestResult'
        self.NameSingle='NoiseSummary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        RocNumbers = array.array('d')
        NoiseList = array.array('d')

        Maximum = 0
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            Noise = float(ChipTestResultObject.ResultData['SubTestResults']['SCurveWidths_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['KeyValueDictPairs']['mu']['Value'])
            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            RocNumbers.append(ChipNo)
            NoiseList.append(Noise)
            if Noise > Maximum:
                Maximum = Noise
             
        self.ResultData['Plot']['ROOTGraph'] = ROOT.TGraph(len(RocNumbers), RocNumbers, NoiseList)

        if self.ResultData['Plot']['ROOTGraph']:
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTGraph'].SetTitle("")
            self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().SetTitle("ROC")
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTGraph'].SetLineColor(ROOT.kMagenta+2)
            self.ResultData['Plot']['ROOTGraph'].SetMarkerColor(ROOT.kMagenta+2)
            self.ResultData['Plot']['ROOTGraph'].SetMarkerStyle(ROOT.kFullSquare)

            if Maximum < self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_B']*1.1:
                self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetRangeUser(0, self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_B']*1.1)
            
            self.ResultData['Plot']['ROOTGraph'].Draw('APL')
            
            lineB = ROOT.TLine().DrawLine(
                0, self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_B'],
                len(RocNumbers), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold_B'],
            )
            lineB.SetLineWidth(2)
            lineB.SetLineStyle(2)
            lineB.SetLineColor(ROOT.kRed)

            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTGraph']

        self.Title = 'Noise {Rate}'.format(Rate=self.Attributes['Rate'])
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()