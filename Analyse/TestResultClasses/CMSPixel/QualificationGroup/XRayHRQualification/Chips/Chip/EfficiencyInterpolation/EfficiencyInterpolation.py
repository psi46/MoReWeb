# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_EfficiencyInterpolation_TestResult'
        self.NameSingle = 'EfficiencyInterpolation'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'InterpolatedEfficiency50': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Interpol. Efficiency 50'
            },
            'InterpolatedEfficiency120': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Interpol. Efficiency 120'
            },
        }
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        PixelArea = 150 * 100 * 1.e-8
        RealHitrateList = array.array('d', [0])
        EfficiencyList = array.array('d', [100])
        ScalingFactor = 1e-6

        DoubleColumnRateList = array.array('d')
        DoubleColumnEfficiencyList = array.array('d')

        for Rate in Rates['HREfficiency']:
            Ntrig = self.ParentObject.ParentObject.ParentObject.Attributes['Ntrig']['HREfficiency_{:d}'.format(Rate)]
            EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{:d}'.format(Rate)].ResultData['Plot']['ROOTObject']
            BackgroundMapROOTObject = self.ParentObject.ResultData['SubTestResults']['BackgroundMap_{:d}'.format(Rate)].ResultData['Plot']['ROOTObject']

            for DoubleColumn in range(1, 25):
                PixelRateList = array.array('d')
                PixelEfficiencyList = array.array('d')

                for PixNo in range(0, 160):
                    col = DoubleColumn * 2 + (1 if PixNo > 79 else 0)
                    row = PixNo % 80
                    PixelNHits = EfficiencyMapROOTObject.GetBinContent(col + 1, row + 1)
                    BackgroundMapNHits = BackgroundMapROOTObject.GetBinContent(col + 1, row + 1)

                    # only count alive pixels
                    if PixelNHits > 0:
                        PixelEfficiency = PixelNHits/Ntrig
                        AreaFactor = 1 * (2 if col==0 or col==51 else 1) * (2 if row==0 or row==79 else 1)

                        # in MHz/cm2
                        PixelRate = BackgroundMapNHits / (25 * 1e-9 * Ntrig * 4160 * PixelArea * AreaFactor) * ScalingFactor

                        PixelRateList.append(PixelRate)
                        PixelEfficiencyList.append(PixelEfficiency)

                DoubleColumnMeanEfficiency = ROOT.TMath.Mean(len(PixelEfficiencyList), PixelEfficiencyList)

                # correct measured hit rate by efficiency
                DoubleColumnRateList.append(ROOT.TMath.Mean(len(PixelRateList), PixelRateList) / DoubleColumnMeanEfficiency)
                
                # in %
                DoubleColumnEfficiencyList.append(DoubleColumnMeanEfficiency * 100)

        self.Canvas.Clear()
        
        self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(DoubleColumnRateList),DoubleColumnRateList,DoubleColumnEfficiencyList)
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            
            cubicFit = ROOT.TF1("fitfunction", "[0]-[1]*x^3", 40, 150)
            cubicFit.SetParameter(1, 100)
            cubicFit.SetParameter(2, 5e-7)
            
            PlotMinEfficiency = 80
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(PlotMinEfficiency, 105.);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, 300);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Hitrate [MHz/cm2]");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Efficiency [%]");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw("ap");

            self.ResultData['Plot']['ROOTObject'].Fit(cubicFit,'QR')
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            InterpolationFunction = cubicFit
            
            for InterpolationRate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
                line = ROOT.TLine().DrawLine(
                    InterpolationRate * 1e6 * ScalingFactor, PlotMinEfficiency,
                    InterpolationRate * 1e6 * ScalingFactor, 100)
                line.SetLineWidth(2)
                line.SetLineStyle(2)
                line.SetLineColor(ROOT.kRed)

                self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency%d'%int(InterpolationRate)]['Value'] = '{:1.2f}'.format(InterpolationFunction.Eval(InterpolationRate * 1e6 * ScalingFactor))
                self.ResultData['KeyList'] += ['InterpolatedEfficiency%d'%int(InterpolationRate)] 



        self.Title = 'Efficiency Interpolation: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        


