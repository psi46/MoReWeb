# -*- coding: utf-8 -*-
import ROOT

from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationPedestal_TestResult'
        self.NameSingle = 'PHCalibrationPedestal'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

    def PopulateResultData(self):

        ROOT.gPad.SetLogy(1)
        self.ResultData['Plot']['ROOTObject_hPedestal'] = \
            self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['Plot'][
                'ROOTObject_hPedestal']
        self.ResultData['Plot']['ROOTObject_rPedestal'] = \
            self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['Plot'][
                'ROOTObject_rPedestal']

        # mP
        MeanPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].GetMean()
        # sP
        # RMSPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].GetRMS()
        # nP
        # IntegralPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(
        #     self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetFirst(),
        #     self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetLast()
        # )
        #nP_entries
        IntegralPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].GetEntries()
        # Calculation of area where are XX% of the events inside...
        # starting from predicted mean bin.
        if IntegralPedestal > 0:

            # -- restricted RMS
            xLow = -1000
            xUp = 1000
            tmpIntegral = 0
            extra = 0

            MeanPedestal_bin = self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().FindBin(MeanPedestal)
            i = 0
            while tmpIntegral < self.TestResultEnvironmentObject.GradingParameters['pedDistribution']:
                xLow = MeanPedestal_bin - i
                xUp = MeanPedestal_bin + i
                tmpIntegral = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(xLow, xUp) / IntegralPedestal

                extra = xUp - xLow
                i += 1
        else:
            xLow = -300
            xUp = 600
            extra = 0

        under = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(0, xLow - extra)
        #print self.Name + ' Warning!! Line 64 needs to be fixed'
        over = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(int(xUp + 1.5 * extra), self.ResultData['Plot'][
            'ROOTObject_hPedestal'].GetNbinsX())

        self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().SetRange(int(xLow - extra), int(xUp + 1.5 * extra))

        IntegralPedestal = self.ResultData['Plot']['ROOTObject_hPedestal'].Integral(
            self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetFirst(),
            self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().GetLast()
        )

        bin_ped_min = int(xLow - extra)
        self.ResultData['HiddenData']['PedestalMin'] = self.ResultData['Plot']['ROOTObject_hPedestal'].GetBinCenter(
            bin_ped_min)
        bin_ped_max = int(xUp + 1.5 * extra)
        self.ResultData['HiddenData']['PedestalMax'] = self.ResultData['Plot']['ROOTObject_hPedestal'].GetBinCenter(
            bin_ped_max)

        self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().SetTitle("Vcal offset")
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetYaxis().SetTitle("No. of Entries")
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetYaxis().SetTitleOffset(1.2)
        self.ResultData['Plot']['ROOTObject_hPedestal'].GetYaxis().CenterTitle()

        self.ResultData['Plot']['ROOTObject_hPedestal'].Draw()

        self.ResultData['Plot']['ROOTObject_rPedestal'].Add(self.ResultData['Plot']['ROOTObject_hPedestal'])
        self.ResultData['Plot']['ROOTObject_rPedestal'].GetXaxis().SetRange(xLow, xUp)

        MeanPedestal = self.ResultData['Plot']['ROOTObject_rPedestal'].GetMean()
        RMSPedestal = self.ResultData['Plot']['ROOTObject_rPedestal'].GetRMS()

        self.ResultData['Plot']['ROOTObject_rPedestal'].SetFillColor(ROOT.kRed)
        self.ResultData['Plot']['ROOTObject_rPedestal'].SetFillStyle(3002)
        self.ResultData['Plot']['ROOTObject_rPedestal'].Draw("same")

        Line = ROOT.TLine()
        line1 = Line.DrawLine(
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xLow), 0,
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xLow),
            0.8 * self.ResultData['Plot']['ROOTObject_rPedestal'].GetMaximum()
        )
        line1.SetLineColor(ROOT.kBlue)
        line1.SetLineWidth(3)
        line1.SetLineStyle(2)
        line2 = Line.DrawLine(
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xUp), 0,
            self.ResultData['Plot']['ROOTObject_rPedestal'].GetBinCenter(xUp),
            0.8 * self.ResultData['Plot']['ROOTObject_rPedestal'].GetMaximum()
        )
        line2.SetLineColor(ROOT.kBlue)
        line2.SetLineWidth(3)
        line2.SetLineStyle(2)

        self.ResultData['Plot']['Caption'] = 'PH Calibration: Pedestal (Vcal)'
        self.SaveCanvas()
        self.ResultData['KeyValueDictPairs'] = {
            'N': {
                'Value': '{0:1.0f}'.format(IntegralPedestal),
                'Label': 'N'
            },
            'mu': {
                'Value': '{0:1.2f}'.format(MeanPedestal),
                'Label': 'μ'
            },
            'mu_electrons': {
                'Value': '{0:1.2f}'.format(MeanPedestal * self.TestResultEnvironmentObject.GradingParameters[
                    'StandardVcal2ElectronConversionFactor']),
                'Label': 'μ_electrons'
            },
            'sigma_electrons': {
                'Value': '{0:1.2f}'.format(RMSPedestal * self.TestResultEnvironmentObject.GradingParameters[
                    'StandardVcal2ElectronConversionFactor']),
                'Label': 'σ_electrons'
            },
            'sigma': {
                'Value': '{0:1.2f}'.format(RMSPedestal),
                'Label': 'RMS'
            }
        }
        self.ResultData['KeyList'] = ['N', 'mu', 'sigma', 'mu_electrons', 'sigma_electrons']

        if under:
            self.ResultData['KeyValueDictPairs']['under'] = {'Value': '{0:1.2f}'.format(under), 'Label': '<='}
            self.ResultData['KeyList'].append('under')
        if over:
            self.ResultData['KeyValueDictPairs']['over'] = {'Value': '{0:1.2f}'.format(over), 'Label': '>='}
            self.ResultData['KeyList'].append('over')

        if self.isPROC:
            for ChannelNumber in range(4):
                h = self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['Plot']['ROOTObject_hPedestal_c%d'%ChannelNumber]
                self.ResultData['KeyValueDictPairs']['mu_RMS_c%d'%ChannelNumber]= {'Label': 'μ/RMS ch%d'%ChannelNumber, 'Value': '{mu:1.2f}/{rms:1.2f}'.format(mu=h.GetMean(), rms=h.GetRMS())}
                self.ResultData['KeyList'].append('mu_RMS_c%d'%ChannelNumber)

        ROOT.gPad.SetLogy(0)