# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_EfficiencyDistribution_TestResult'
        self.NameSingle = 'EfficiencyDistribution'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'N': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'N'
            },
            'mu': {
                'Value':'{0:1.2f}'.format(-1),
                'Label':'μ'
            },
            'sigma':{
                'Value':'{0:1.2f}'.format(-1),
                'Label':'σ'
            }
        }
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
        Ntrig = self.ParentObject.ParentObject.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=self.Attributes['Rate'])]
        MaximumValue = EfficiencyMapROOTObject.GetMaximum()*100.0/float(Ntrig)
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(),'',int(MaximumValue+1),0,MaximumValue+1)
        
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            for Row in range(self.nRows):
                for Column in range(self.nCols):
                    self.ResultData['Plot']['ROOTObject'].Fill(EfficiencyMapROOTObject.GetBinContent(Column+1, Row+1)*100.0/float(Ntrig))

            #self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.1, 1.2 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Efficiency");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();

            #mN
            Mean = self.ResultData['Plot']['ROOTObject'].GetMean()
            #sN
            RMS = self.ResultData['Plot']['ROOTObject'].GetRMS()
            #nN
            Integral = self.ResultData['Plot']['ROOTObject'].Integral(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
            )
            
            self.ResultData['KeyValueDictPairs']['N']['Value'] = '{0:1.0f}'.format(Integral)
            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.2f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['N','mu','sigma']
            

        self.Title = 'Efficiency Distr. {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        ROOT.gPad.SetLogy(1)
        self.SaveCanvas()
        ROOT.gPad.SetLogy(0)


