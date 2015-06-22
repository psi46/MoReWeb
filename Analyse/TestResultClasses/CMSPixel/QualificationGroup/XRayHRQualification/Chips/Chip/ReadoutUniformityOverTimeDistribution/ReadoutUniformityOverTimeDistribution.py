# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import math

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_ReadoutUniformityOverTimeDistribution_TestResult'
        self.NameSingle = 'ReadoutUniformityOverTimeDistribution'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'chi2/ndf': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'chi2/ndf'
            },
            'sigma':{
                'Value':'{0:1.2f}'.format(-1),
                'Label':'σ'
            },
            'sigma_th':{
                'Value':'{0:1.2f}'.format(-1),
                'Label':'σ_th'
            }
        }
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        UniformityOverTimePlot = self.ParentObject.ResultData['SubTestResults']['ReadoutUniformityOverTime_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']

        if UniformityOverTimePlot:
            EventsMaximum = UniformityOverTimePlot.GetMaximum()
            distribution = ROOT.TH1D(self.GetUniqueID(),'', 256, 0, EventsMaximum + 1)
            for i in range(1, UniformityOverTimePlot.FindLastBinAbove(0)):
                distribution.Fill(UniformityOverTimePlot.GetBinContent(i))

            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'] = distribution.Clone(self.GetUniqueID())
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].Draw()

            poisson = ROOT.TF1("poisson", "TMath::PoissonI(x,%f)*%f"%(distribution.GetMean(),float(UniformityOverTimePlot.GetNbinsX())*distribution.GetBinWidth(1)),0,EventsMaximum)
            
            sigma = distribution.GetRMS()
            sigma_th = math.sqrt(distribution.GetMean())

            chi2 = 0
            ndf = 0
            for i in range(1, distribution.GetNbinsX()+1):
                Ei = poisson.Eval(distribution.GetBinCenter(i))
                # exclude areas < 1 events expected
                if Ei > 0.5:
                    chi2 += (distribution.GetBinContent(i) - Ei)*(distribution.GetBinContent(i) - Ei)/Ei
                    ndf += 1

            chi2ndf_max = 99999

            if ndf < 3:
                chi2ndf = chi2ndf_max
            else:
                chi2ndf = chi2 / (ndf - 2)

            if chi2ndf > chi2ndf_max:
                chi2ndf = chi2ndf_max

            poisson.Draw("same")

            self.ResultData['KeyValueDictPairs']['chi2/ndf']['Value'] = '{0:1.2f}'.format(chi2ndf)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(sigma)
            self.ResultData['KeyValueDictPairs']['sigma_th']['Value'] = '{0:1.2f}'.format(sigma_th)

            self.ResultData['KeyList'] += ['chi2/ndf', 'sigma', 'sigma_th']

        self.Title = 'Time unif. distribution {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        self.SaveCanvas() 
