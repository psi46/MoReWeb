import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_EfficiencyDistribution_TestResult'
        self.NameSingle='EfficiencyDistribution'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(1)
        ROOT.gStyle.SetOptStat(0)

        EfficiencyOverview = self.ParentObject.ResultData['SubTestResults']['EfficiencyOverview_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
        Ntrig = self.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=self.Attributes['Rate'])]

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", 100, 0, 100.01)

        for col in range(self.nCols*8): 
            for row in range(self.nRows*2):
                result = EfficiencyOverview.GetBinContent(col + 1, row + 1)
                self.ResultData['Plot']['ROOTObject'].Fill(result*100.0/Ntrig)

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("efficiency")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].Draw('')

        self.Title = 'Efficiency distribution {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()
        ROOT.gPad.SetLogy(0)