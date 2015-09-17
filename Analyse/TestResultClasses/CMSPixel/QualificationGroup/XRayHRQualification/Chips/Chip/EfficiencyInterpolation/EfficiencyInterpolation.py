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
        self.FitFunction = "[0]-[1]*x^3"
        self.ResultData['KeyValueDictPairs'] = {}
        for Rate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}'.format(Rate=Rate)] = {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Interpol. Efficiency {Rate}'.format(Rate=Rate)
            }
        self.ResultData['KeyValueDictPairs']['fitfunction'] = {
            'Value': self.FitFunction,
            'Label':'Fit'.format(Rate=Rate)
        }
        self.ResultData['KeyList'].append('fitfunction')
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        PixelArea = 150 * 100 * 1.e-8
        RealHitrateList = array.array('d', [0])
        EfficiencyList = array.array('d', [100])
        ScalingFactor = 1e-6
        HiddenDataInterpolationRates = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
        for InterpolationRate in HiddenDataInterpolationRates:
            self.ResultData['HiddenData']['InterpolatedEfficiency%d'%int(InterpolationRate)] = {
                'Label': 'Interpolated Efficiency at %s Mhz/cm2'%int(InterpolationRate),
                'Value': '0',
                'Unit': '%',
            }

        DoubleColumnRateList = array.array('d')
        DoubleColumnEfficiencyList = array.array('d')

        for Rate in Rates['HREfficiency']:
            Ntrig = self.ParentObject.ParentObject.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)]
            EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            BackgroundMapROOTObject = self.ParentObject.ResultData['SubTestResults']['BackgroundMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']

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

                try:
                    DoubleColumnMeanEfficiency = ROOT.TMath.Mean(len(PixelEfficiencyList), PixelEfficiencyList)
                    DoubleColumnRate = ROOT.TMath.Mean(len(PixelRateList), PixelRateList)
                    # correct measured hit rate by efficiency, in %
                    DoubleColumnRateList.append(DoubleColumnRate / DoubleColumnMeanEfficiency)
                    DoubleColumnEfficiencyList.append(DoubleColumnMeanEfficiency * 100)
                except:
                    pass



        self.Canvas.Clear()

        if len(DoubleColumnRateList) > 0:
            self.ResultData['Plot']['ROOTObject'] = ROOT.TGraph(len(DoubleColumnRateList), DoubleColumnRateList,DoubleColumnEfficiencyList)

            if self.ResultData['Plot']['ROOTObject']:
                ROOT.gStyle.SetOptStat(0)

                cubicFit = ROOT.TF1("fitfunction", self.FitFunction, 40, 150)
                cubicFit.SetParameter(1, 100)
                cubicFit.SetParameter(2, 5e-7)

                PlotMinEfficiency = 80
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(PlotMinEfficiency, 105.)
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, 300)
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Hitrate [MHz/cm2]")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Efficiency [%]")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw("ap")

                self.ResultData['Plot']['ROOTObject'].Fit(cubicFit,'QR')
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                InterpolationFunction = cubicFit

                # values to show in summary
                for InterpolationRate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
                    line = ROOT.TLine().DrawLine(
                        InterpolationRate * 1e6 * ScalingFactor, PlotMinEfficiency,
                        InterpolationRate * 1e6 * ScalingFactor, 100)
                    line.SetLineWidth(2)
                    line.SetLineStyle(2)
                    line.SetLineColor(ROOT.kRed)

                    self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency%d'%int(InterpolationRate)]['Value'] = '{InterpolatedEfficiency:1.2f}'.format(InterpolatedEfficiency=InterpolationFunction.Eval(InterpolationRate * 1e6 * ScalingFactor))
                    self.ResultData['KeyList'] += ['InterpolatedEfficiency%d'%int(InterpolationRate)]

                # always interpolate at this rates, but don't show them in summary
                for InterpolationRate in HiddenDataInterpolationRates:
                    self.ResultData['HiddenData']['InterpolatedEfficiency%d'%int(InterpolationRate)]['Value'] = '{InterpolatedEfficiency:1.2f}'.format(InterpolatedEfficiency=InterpolationFunction.Eval(InterpolationRate * 1e6 * ScalingFactor))

        else:
                for InterpolationRate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
                    self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency%d'%int(InterpolationRate)]['Value'] = '{InterpolatedEfficiency:1.2f}'.format(InterpolatedEfficiency=0)
                    self.ResultData['KeyList'] += ['InterpolatedEfficiency%d'%int(InterpolationRate)]

        self.Title = 'Efficiency Interpolation: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        

