import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XrayCalibrationSpectrum_HitmapDistribution_TestResult'
        self.NameSingle='HitmapDistribution'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogx(1)
        ROOT.gStyle.SetOptStat(0)

        HitMapOverview = self.ParentObject.ResultData['SubTestResults']['HitmapOverview_{Target}'.format(Target=self.Attributes['Target'])].ResultData['Plot']['ROOTObject']

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", int((HitMapOverview.GetMaximum()*1.05-HitMapOverview.GetMinimum())), float(HitMapOverview.GetMinimum()), float(HitMapOverview.GetMaximum()*1.05))
        GraphEdges = ROOT.TH1D(self.GetUniqueID(), "", int((HitMapOverview.GetMaximum()*1.05-HitMapOverview.GetMinimum())), float(HitMapOverview.GetMinimum()), float(HitMapOverview.GetMaximum()*1.05))
        GraphCorners = ROOT.TH1D(self.GetUniqueID(), "", int((HitMapOverview.GetMaximum()*1.05-HitMapOverview.GetMinimum())), float(HitMapOverview.GetMinimum()), float(HitMapOverview.GetMaximum()*1.05))

        for col in range(self.nCols*8):
            for row in range(self.nRows*2):
                result = HitMapOverview.GetBinContent(col + 1, row + 1)
                if (col % 52 == 0 or col % 52 == 51) and (row % 80 == 0 or row % 80 == 79):
                    GraphCorners.Fill(result)
                elif (col % 52 == 0 or col % 52 == 51) or (row % 80 == 0 or row % 80 == 79):
                    GraphEdges.Fill(result)
                else:
                    self.ResultData['Plot']['ROOTObject'].Fill(result)


        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("#hits")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue)
            self.ResultData['Plot']['ROOTObject'].Draw('')

            GraphEdges.SetTitle("")
            GraphEdges.GetXaxis().SetTitle("")
            GraphEdges.GetYaxis().SetTitle("")
            GraphEdges.SetLineColor(ROOT.kGreen+2)
            GraphEdges.Draw('SAME')

            GraphCorners.SetTitle("")
            GraphCorners.GetXaxis().SetTitle("")
            GraphCorners.GetYaxis().SetTitle("")
            GraphCorners.SetLineColor(ROOT.kRed)
            GraphCorners.Draw('SAME')


        self.Title = 'Hits distribution {Target} inner/edge/corner'.format(Target=self.Attributes['Target'])
        self.SaveCanvas()
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)