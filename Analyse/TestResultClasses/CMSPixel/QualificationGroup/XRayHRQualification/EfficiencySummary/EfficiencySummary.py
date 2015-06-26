import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_EfficiencySummary_TestResult'
        self.NameSingle='EfficiencySummary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)

        RocNumbers = array.array('d')
        Efficiencies = array.array('d')

        Minimum = 100
        Maximum = 0
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            Efficiency = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Efficiency_{Rate}'.format(Rate=self.Attributes['Rate'])]
            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            RocNumbers.append(ChipNo)
            Efficiencies.append(Efficiency)
            if Efficiency < Minimum:
                Minimum = Efficiency
            if Efficiency > Maximum:
                Maximum = Efficiency
             
        self.ResultData['Plot']['ROOTGraph'] = ROOT.TGraph(len(RocNumbers), RocNumbers, Efficiencies)

        try:
            RateIndex = 1 + self.ParentObject.Attributes['InterpolatedEfficiencyRates'].index(int(self.Attributes['Rate']))
        except:
            RateIndex = 0
            
        if self.ResultData['Plot']['ROOTGraph']:
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTGraph'].SetTitle("")
            self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().SetTitle("ROC")
            self.ResultData['Plot']['ROOTGraph'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTGraph'].SetLineColor(ROOT.kGreen+2)
            self.ResultData['Plot']['ROOTGraph'].SetMarkerColor(ROOT.kGreen+2)
            self.ResultData['Plot']['ROOTGraph'].SetMarkerStyle(ROOT.kFullSquare)

            self.ResultData['Plot']['ROOTGraph'].Draw('APL')

            if RateIndex > 0:
                GradeABThreshold = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_A_Rate{RateIndex}'.format(RateIndex=RateIndex)]
                GradeBCThreshold = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_max_allowed_loweff_B_Rate{RateIndex}'.format(RateIndex=RateIndex)]
            
                if Minimum > GradeABThreshold:
                    self.ResultData['Plot']['ROOTGraph'].GetYaxis().SetRangeUser(GradeABThreshold * 0.995, Maximum * 1.005)

                lineB = ROOT.TLine().DrawLine(0, GradeABThreshold, len(RocNumbers), GradeABThreshold)
                lineB.SetLineWidth(2)
                lineB.SetLineStyle(2)
                lineB.SetLineColor(ROOT.kRed)

                if Minimum < GradeBCThreshold:
                    lineC = ROOT.TLine().DrawLine(0, GradeBCThreshold, len(RocNumbers), GradeBCThreshold)
                    lineC.SetLineWidth(2)
                    lineC.SetLineStyle(2)
                    lineC.SetLineColor(ROOT.kRed)

            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTGraph']

        self.Title = 'Efficiency at {Rate} MHz/cm2'.format(Rate=self.Attributes['Rate'])
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()