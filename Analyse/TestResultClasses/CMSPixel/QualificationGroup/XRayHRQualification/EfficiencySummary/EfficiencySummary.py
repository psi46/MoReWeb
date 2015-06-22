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
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            Efficiency = ChipTestResultObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Efficiency_{Rate}'.format(Rate=self.Attributes['Rate'])]
            ChipNo = ChipTestResultObject.Attributes['ChipNo']
            RocNumbers.append(ChipNo)
            Efficiencies.append(Efficiency)
            if Efficiency < Minimum:
                Minimum = Efficiency
             
        self.ResultData['Plot']['ROOTGraph'] = ROOT.TGraph(len(RocNumbers), RocNumbers, Efficiencies)

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

            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTGraph']

        self.Title = 'Efficiency at {Rate} MHz/cm2'.format(Rate=self.Attributes['Rate'])
        self.ResultData['Plot']['Format'] = 'svg'
        self.SaveCanvas()