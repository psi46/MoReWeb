# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'DoubleColumnEfficiencyDistribution'
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {}
        
        
    def PopulateResultData(self):
        self.Canvas.Clear()

        ChipNo = self.ParentObject.Attributes['ChipNo']
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        PixelArea = 150 * 100 * 1.e-8
        RealHitrateList = array.array('d', [0])
        EfficiencyList = array.array('d', [100])
        ScalingFactor = 1e-6

        RootHistograms = []

        First = True
        CurveColors = [ROOT.kBlue+2,ROOT.kRed+1, ROOT.kGreen+3]
        ColorIndex = 0
        for InterpolationRate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            RootHistogram = ROOT.TH1D(self.GetUniqueID(), '', 50, 95, 100)

            for DoubleColumn in range(1, 25):
                DoubleColumnRateList = array.array('d')
                DoubleColumnEfficiencyList = array.array('d')

                for Rate in Rates['HREfficiency']:
                    Ntrig = self.ParentObject.ParentObject.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)]
                    EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
                    BackgroundMapROOTObject = self.ParentObject.ResultData['SubTestResults']['BackgroundMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']

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
                        print "could not calculate double column efficiency: ROC", ChipNo, " DC:", DoubleColumn

                try:
                    cubicFit = ROOT.TF1("fitfunction", "[0]-[1]*x^3", 40, 150)
                    cubicFit.SetParameter(1, 100)
                    cubicFit.SetParameter(2, 5e-7)

                    EfficiencyGraph = ROOT.TGraph(len(DoubleColumnRateList), DoubleColumnRateList, DoubleColumnEfficiencyList)
                    EfficiencyGraph.Fit(cubicFit, 'QR')

                    RootHistogram.Fill(cubicFit.Eval(InterpolationRate * 1.0e6 * ScalingFactor))
                    cubicFit.Delete()
                    EfficiencyGraph.Delete()
                except:
                    print "warning: ROC",ChipNo," double column ", DoubleColumn, ": efficiency fit failed!"

            if RootHistogram:
                RootHistogram.SetLineColor(CurveColors[ColorIndex])
                ColorIndex += 1
                if ColorIndex > len(CurveColors)-1:
                    ColorIndex = 0
                if First:
                    RootHistogram.Draw("")
                    First = False
                else:
                    RootHistogram.Draw("same")
                RootHistograms.append(RootHistogram)

        Legend = ROOT.TLegend(0.2,0.85,0.4,0.65)
        for i in range(len(RootHistograms)):
            Legend.AddEntry(RootHistograms[i], '%d MHz/cm2'%self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates'][i], 'l')
        Legend.Draw("")
        ROOT.gPad.Update()

        self.Title = 'DC Efficiency Distribution: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()

        try:
            for i in RootHistograms:
                i.Delete()
        except:
            pass


