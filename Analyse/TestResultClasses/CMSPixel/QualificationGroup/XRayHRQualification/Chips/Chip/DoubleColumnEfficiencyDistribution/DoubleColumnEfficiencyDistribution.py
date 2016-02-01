# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'DoubleColumnEfficiencyDistribution'
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {}
        self.ResultData['KeyValueDictPairs']['NBadDoubleColumns'] = {
            'Label': 'Bad Double Columns',
            'Value': '-1'
        }

        
    def PopulateResultData(self):
        self.Canvas.Clear()

        ChipNo = self.ParentObject.Attributes['ChipNo']
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        PixelArea = 150 * 100 * 1.e-8
        ScalingFactor = 1e-6

        BAD_DOUBLECOLUMN_DATA = 1
        BAD_DOUBLECOLUMN_FIT = 2
        BAD_DOUBLECOLUMN_EFF = 4
        
        MinDCEfficiencyFiducial = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_fiducial_dc_eff']
        MinDCEfficiencyEdge = self.TestResultEnvironmentObject.GradingParameters['XRayHighRateEfficiency_min_fiducial_dc_eff']

        # calculate efficiencies for all rates
        DoubleColumnEfficiencies = []
        BadDoubleColumns = []
        NonEmptyDoubleColumnFound = False
        for InterpolationRate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
            DoubleColumnEfficienciesRate = []
            FiducialDoubleColumnEfficienciesRate = []

            # and all double columns
            for DoubleColumn in range(0, 26):
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
                        DoubleColumnMeanEfficiencyPercent = DoubleColumnMeanEfficiency * 100
                        DoubleColumnEfficiencyList.append(DoubleColumnMeanEfficiencyPercent)

                    except:
                        BadDoubleColumns.append({'Chip': ChipNo, 'DoubleColumn': DoubleColumn, 'Error': BAD_DOUBLECOLUMN_DATA})


                try:
                    if len(DoubleColumnRateList) > 0:
                        cubicFit = ROOT.TF1("fitfunction", "[0]-[1]*x^3", 5, 150)
                        cubicFit.SetParameter(0, 100.0)
                        cubicFit.SetParLimits(0, 0.0, 110.0)
                        cubicFit.SetParameter(1, 5.0e-7)
                        cubicFit.SetParLimits(1, 0, 1.0e-5)

                        EfficiencyGraph = ROOT.TGraph(len(DoubleColumnRateList), DoubleColumnRateList, DoubleColumnEfficiencyList)
                        EfficiencyGraph.Fit(cubicFit, 'QRB')
                        InterpolatedEfficiency = cubicFit.Eval(InterpolationRate * 1.0e6 * ScalingFactor)

                        if InterpolationRate < 121:
                            if DoubleColumn in [0,25]:
                                if InterpolatedEfficiency*0.01 < MinDCEfficiencyEdge:
                                    print "        Edge DC with bad efficiency found!"
                                    print "            rates:", DoubleColumnRateList
                                    print "            eff:", DoubleColumnEfficiencyList

                                    print "        -> e(120MHz/cm2) =  ", InterpolatedEfficiency
                                    BadDoubleColumns.append({'Chip': ChipNo, 'DoubleColumn': DoubleColumn, 'Error': BAD_DOUBLECOLUMN_EFF})
                            else:
                                if InterpolatedEfficiency*0.01 < MinDCEfficiencyFiducial:
                                    print "        DC with bad efficiency found!"
                                    print "            rates:", DoubleColumnRateList
                                    print "            eff:", DoubleColumnEfficiencyList

                                    print "        -> e(120MHz/cm2) =  ", InterpolatedEfficiency
                                    BadDoubleColumns.append({'Chip': ChipNo, 'DoubleColumn': DoubleColumn, 'Error': BAD_DOUBLECOLUMN_EFF})

                        DoubleColumnEfficienciesRate.append(InterpolatedEfficiency)
                        if DoubleColumn not in [0, 25]:
                            FiducialDoubleColumnEfficienciesRate.append(InterpolatedEfficiency)
                        cubicFit.Delete()
                        EfficiencyGraph.Delete()
                        NonEmptyDoubleColumnFound = True

                except:
                    BadDoubleColumns.append({'Chip': ChipNo, 'DoubleColumn': DoubleColumn, 'Error': BAD_DOUBLECOLUMN_FIT})

            DoubleColumnEfficiencies.append(DoubleColumnEfficienciesRate)

            self.ResultData['KeyValueDictPairs']['MeanEfficiency_%d'%InterpolationRate] = {'Value': '-1', 'Label': 'Mean Efficiency %d MHz/cm2'%InterpolationRate}
            try:
                MeanEfficiency = sum(FiducialDoubleColumnEfficienciesRate)/len(FiducialDoubleColumnEfficienciesRate) if len(FiducialDoubleColumnEfficienciesRate) > 0 else 0
                self.ResultData['KeyValueDictPairs']['MeanEfficiency_%d'%InterpolationRate]['Value'] = '{MeanEfficiency:1.2f}'.format(MeanEfficiency=MeanEfficiency)
                self.ResultData['KeyList'].append('MeanEfficiency_%d'%InterpolationRate)
            except:
                pass


        # get minimum efficiency
        AllDoubleColumnEfficiencies = [item for sublist in DoubleColumnEfficiencies for item in sublist]
        try:
            EfficiencyPlotMinimum = min(95, min(AllDoubleColumnEfficiencies))
        except:
            EfficiencyPlotMinimum = 95

        # draw histogram for each of the different rates with different color
        RootHistograms = []
        First = True
        CurveColors = [ROOT.kBlue+2,ROOT.kRed+1, ROOT.kGreen+3]
        ColorIndex = 0
        for DoubleColumnEfficienciesRate in DoubleColumnEfficiencies:
            RootHistogram = ROOT.TH1D(self.GetUniqueID(), '', 1000, 0, 100)
            RootHistogram.GetXaxis().SetRangeUser(EfficiencyPlotMinimum, 100)

            for DoubleColumnEfficiency in DoubleColumnEfficienciesRate:
                RootHistogram.Fill(DoubleColumnEfficiency)

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

        self.ResultData['HiddenData']['BadDoubleColumns'] = BadDoubleColumns
        if NonEmptyDoubleColumnFound:
            self.ResultData['KeyValueDictPairs']['NBadDoubleColumns']['Value'] = len(set([BadDoubleColumn['DoubleColumn'] for BadDoubleColumn in BadDoubleColumns]))

        self.ResultData['KeyList'].append('NBadDoubleColumns')

        try:
            for i in RootHistograms:
                i.Delete()
        except:
            pass


