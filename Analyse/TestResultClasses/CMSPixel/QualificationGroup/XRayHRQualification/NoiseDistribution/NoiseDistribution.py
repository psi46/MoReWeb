import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_NoiseDistribution_TestResult'
        self.NameSingle='NoiseDistribution'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(1)
        ROOT.gStyle.SetOptStat(0)

        NoiseOverview = self.ParentObject.ResultData['SubTestResults']['NoiseOverview_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", int((NoiseOverview.GetMaximum()*1.05-NoiseOverview.GetMinimum()) / 10), float(NoiseOverview.GetMinimum()), float(NoiseOverview.GetMaximum()*1.05))

        for col in range(self.nCols*8): 
            for row in range(self.nRows*2):
                result = NoiseOverview.GetBinContent(col + 1, row + 1)
                self.ResultData['Plot']['ROOTObject'].Fill(result)
                

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("electrons")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].Draw('')

        self.Title = 'Noise distribution {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()
        ROOT.gPad.SetLogy(0)