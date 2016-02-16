# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
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
            self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency{Rate}Error'.format(Rate=Rate)] = {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'Interpol. Efficiency {Rate} error'.format(Rate=Rate)
            }
        self.ResultData['KeyValueDictPairs']['fitfunction'] = {
            'Value': self.FitFunction,
            'Label':'Fit'.format(Rate=Rate)
        }
        self.ResultData['KeyList'].append('fitfunction')
        self.ResultData['KeyValueDictPairs']['BadDoubleColumns'] = {
            'Value': '',
            'Label':'# Bad DCs (excluded from fit)'
        }
        self.ResultData['KeyList'].append('BadDoubleColumns')
        self.HiddenDataInterpolationRates = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150]
        for InterpolationRate in self.HiddenDataInterpolationRates:
            self.ResultData['HiddenData']['InterpolatedEfficiency%d'%int(InterpolationRate)] = {
                'Label': 'Interpolated Efficiency at %s Mhz/cm2'%int(InterpolationRate),
                'Value': '-1',
                'Unit': '%',
            }
            self.ResultData['HiddenData']['InterpolatedEfficiency%dError'%int(InterpolationRate)] = {
                'Label': 'Interpolated Efficiency at %s Mhz/cm2 error'%int(InterpolationRate),
                'Value': '-1',
                'Unit': '%',
            }
        self.ResultData['KeyValueDictPairs']['Chi2NDF'] = {'Label':'chi2/ndf', 'Value': '-1'}
        self.ResultData['KeyValueDictPairs']['NumberFitPoints'] = {'Label':'# fit points', 'Value': '-1'}

    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        PixelArea = 150 * 100 * 1.e-8
        RealHitrateList = array.array('d', [0])
        EfficiencyList = array.array('d', [100])
        ScalingFactor = 1e-6


        DoubleColumnRateList = array.array('d')
        DoubleColumnEfficiencyList = array.array('d')

        # get list of double columns which have been flagged bad
        try:
            BadDoubleColumns = list(set([DoubleColumnData['DoubleColumn'] for DoubleColumnData in self.ParentObject.ResultData['SubTestResults']['DoubleColumnEfficiencyDistribution'].ResultData['HiddenData']['BadDoubleColumns']]))
        except:
            BadDoubleColumns = []

        self.ResultData['KeyValueDictPairs']['BadDoubleColumns']['Value'] = len(BadDoubleColumns)

        ExcludedMessageShown = []
        for Rate in Rates['HREfficiency']:
            Ntrig = self.ParentObject.ParentObject.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=Rate)]
            EfficiencyMapROOTObject = self.ParentObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']
            BackgroundMapROOTObject = self.ParentObject.ResultData['SubTestResults']['BackgroundMap_{Rate}'.format(Rate=Rate)].ResultData['Plot']['ROOTObject']

            for DoubleColumn in range(1, 25):

                if DoubleColumn not in BadDoubleColumns:
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
                else:
                    if DoubleColumn not in ExcludedMessageShown:
                        print "\x1b[31m         double column %d is flagged 'bad' and excluded from fit\x1b[0m"%DoubleColumn
                        ExcludedMessageShown.append(DoubleColumn)

        self.Canvas.Clear()

        if len(DoubleColumnRateList) > 0:
            DoubleColumnRateErrorsList = array.array('d', [0.5] * len(DoubleColumnRateList))
            DoubleColumnEfficiencyErrorsList = array.array('d', [0.1] * len(DoubleColumnEfficiencyList))
            self.ResultData['Plot']['ROOTObject'] = ROOT.TGraphErrors(len(DoubleColumnRateList), DoubleColumnRateList, DoubleColumnEfficiencyList, DoubleColumnRateErrorsList, DoubleColumnEfficiencyErrorsList)

            if self.ResultData['Plot']['ROOTObject']:
                ROOT.gStyle.SetOptStat(0)

                cubicFit = ROOT.TF1("fitfunction", self.FitFunction, 40, 150)
                cubicFit.SetParameter(0, 100)
                cubicFit.SetParLimits(0, 0, 101)
                cubicFit.SetParameter(1, 5e-7)
                cubicFit.SetParLimits(1, 0, 0.01)

                PlotMinEfficiency = min(80, min(DoubleColumnEfficiencyList)*0.95) if len(DoubleColumnEfficiencyList) > 0 else 80
                RateMaxRange = max(300, max(DoubleColumnRateList)*1.05) if len(DoubleColumnRateList) > 0 else 300
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(PlotMinEfficiency, 105.)
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, RateMaxRange)
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Hitrate [MHz/cm2]")
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Efficiency [%]")
                self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
                self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
                self.ResultData['Plot']['ROOTObject'].Draw("ap")

                FitResults = self.ResultData['Plot']['ROOTObject'].Fit(cubicFit,'BQRS')
                self.ResultData['Plot']['ROOTObject'].SetTitle("")
                InterpolationFunction = cubicFit

                self.ResultData['KeyValueDictPairs']['Chi2NDF']['Value'] = '{0:1.2f}'.format(cubicFit.GetChisquare() / max(cubicFit.GetNDF(), 1))
                self.ResultData['KeyList'].append('Chi2NDF')

                self.ResultData['KeyValueDictPairs']['NumberFitPoints']['Value'] = cubicFit.GetNumberFitPoints()
                self.ResultData['KeyList'].append('NumberFitPoints')

                self.ResultData['KeyValueDictPairs']['p0'] = {'Label':'p0', 'Value': '{0:1.2f}'.format(cubicFit.GetParameter(0))}
                self.ResultData['KeyList'].append('p0')

                self.ResultData['KeyValueDictPairs']['p1'] = {'Label':'p1', 'Value': '{0:1.2e}'.format(cubicFit.GetParameter(1))}
                self.ResultData['KeyList'].append('p1')


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

                    xpos = array.array('d', [float(InterpolationRate * 1.0e6 * ScalingFactor)])
                    err = array.array('d', [0.]*len(xpos))
                    try:
                        FitResults.GetConfidenceIntervals(len(xpos), 1, 1, xpos, err, 0.683)
                        InterpolatedEfficiencyError = err[0]
                    except:
                        InterpolatedEfficiencyError = 0
                        pass
                    self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency%dError'%int(InterpolationRate)]['Value'] = '{InterpolatedEfficiencyError:1.3f}'.format(InterpolatedEfficiencyError=InterpolatedEfficiencyError)
                    #self.ResultData['KeyList'] += ['InterpolatedEfficiency%dError'%int(InterpolationRate)]

                # always interpolate at this rates, but don't show them in summary
                for InterpolationRate in self.HiddenDataInterpolationRates:
                    self.ResultData['HiddenData']['InterpolatedEfficiency%d'%int(InterpolationRate)]['Value'] = '{InterpolatedEfficiency:1.2f}'.format(InterpolatedEfficiency=InterpolationFunction.Eval(InterpolationRate * 1e6 * ScalingFactor))

        else:
                for InterpolationRate in self.ParentObject.ParentObject.ParentObject.Attributes['InterpolatedEfficiencyRates']:
                    self.ResultData['KeyValueDictPairs']['InterpolatedEfficiency%d'%int(InterpolationRate)]['Value'] = '{InterpolatedEfficiency:1.2f}'.format(InterpolatedEfficiency=-1)
                    self.ResultData['KeyList'] += ['InterpolatedEfficiency%d'%int(InterpolationRate)]

        self.Title = 'Efficiency Interpolation: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        

