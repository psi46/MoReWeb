# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import math

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBonding_TestResult'
        self.NameSingle = 'BumpBonding'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.Attributes['isDigitalROC'] = self.ParentObject.ParentObject.ParentObject.Attributes['isDigital']

        self.ResultData['KeyValueDictPairs']['Mean'] = {'Value': -999, 'Label': 'Mean', }
        self.ResultData['KeyValueDictPairs']['RMS'] = {'Value': -1, 'Label': 'RMS', }
        self.ResultData['KeyValueDictPairs']['Threshold'] = {'Value': round(-999, 2), 'Label': 'Threshold', }
        if self.Attributes['isDigitalROC']:
            self.ResultData['KeyValueDictPairs']['nSigma'] = {'Value': -1, 'Label': 'σ'}
            self.ResultData['KeyValueDictPairs']['nBumpBondingProblems'] = {'Value': round(-1, 0),
                                                                            'Label': 'N BumpProblems'}

            self.ResultData['KeyValueDictPairs']['nBumpBondingProblems2'] = {'Value': round(-1, 0),
                                                                            'Label': 'N (experimental cut)',
                                                                            'Style': 'color:#666;'}

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        ROOT.gPad.SetLogy(1)
        mean = -9999
        rms = -9999
        nBumpBondingProblems = 0
        nSigma = self.TestResultEnvironmentObject.GradingParameters['BumpBondingProblemsNSigma']
        thr = 0

        # TH1D
        ChipNo = self.ParentObject.Attributes['ChipNo']
        self.HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        try:
            histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle, 'Analog')
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject'] = object.Clone(self.GetUniqueID())
        except:
            histname = self.ParentObject.ParentObject.ParentObject.HistoDict.get(self.NameSingle, 'Digital')
            object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject'] = object.Clone(self.GetUniqueID())

        if self.ResultData['Plot']['ROOTObject']:
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            if not self.Attributes['isDigitalROC']:
                self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(-50., 50.)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0.5, 5.0 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Threshold difference")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw()

            # cut 1
            mean = self.ResultData['Plot']['ROOTObject'].GetMean()
            rms = self.ResultData['Plot']['ROOTObject'].GetRMS()
            thr = mean + nSigma * rms
            startbin = self.ResultData['Plot']['ROOTObject'].FindBin(thr)
            for bin in range(startbin, self.ResultData['Plot']['ROOTObject'].GetNbinsX()):
                nBumpBondingProblems += self.ResultData['Plot']['ROOTObject'].GetBinContent(bin)
            self.Cut = ROOT.TCutG('bumpBondingThreshold', 2)
            self.Cut.SetPoint(0, thr, -1e9)
            self.Cut.SetPoint(1, thr, +1e9)
            self.Cut.SetLineWidth(2)
            self.Cut.SetLineStyle(2)
            self.Cut.SetLineColor(ROOT.kRed)
            self.Cut.Draw('PL')

            # cut 2 (experimental)
            CoarseHistogram = self.ResultData['Plot']['ROOTObject'].Clone(self.GetUniqueID())
            RebinX = 4
            CoarseHistogram.Rebin(RebinX)
            CoarseHistogram.GetXaxis().SetRangeUser(20, 250)
            PeakPositionGuess = CoarseHistogram.GetXaxis().GetBinLowEdge(CoarseHistogram.GetMaximumBin())

            # 1st iteration
            GaussFitFunction = ROOT.TF1("BBPeakFitFunction","gaus(0)", max(0, PeakPositionGuess), min(PeakPositionGuess+40, 255))
            GaussFitFunction.SetParameter(0, CoarseHistogram.GetBinContent(CoarseHistogram.GetMaximumBin()) / RebinX)
            GaussFitFunction.SetParameter(1, PeakPositionGuess)
            GaussFitFunction.SetParameter(2, 10)
            GaussFitFunction.SetParLimits(2, 1, 30)
            GaussFitFunction.SetLineColor(ROOT.kGreen+3)
            self.ResultData['Plot']['ROOTObject'].Fit(GaussFitFunction, "QBR+")

            thr2 = GaussFitFunction.GetParameter(1) + 4 * GaussFitFunction.GetParameter(2)

            try:
                thrLowLimit = 5 + GaussFitFunction.GetParameter(1) + math.sqrt(2)*GaussFitFunction.GetParameter(2) * math.sqrt(math.log(2) - math.log(1.0/GaussFitFunction.GetParameter(0)))
                if thr2 < thrLowLimit:
                    thr2 = thrLowLimit
            except:
                pass

            startbin = self.ResultData['Plot']['ROOTObject'].FindBin(thr2)
            nBumpBondingProblems2 = 0
            for bin in range(startbin, self.ResultData['Plot']['ROOTObject'].GetNbinsX()):
                nBumpBondingProblems2 += self.ResultData['Plot']['ROOTObject'].GetBinContent(bin)

            self.Cut2 = ROOT.TCutG('bumpBondingThreshold2', 2)
            self.Cut2.SetPoint(0, thr2, -1e9)
            self.Cut2.SetPoint(1, thr2, +1e9)
            self.Cut2.SetLineWidth(3)
            self.Cut2.SetLineStyle(6)
            self.Cut2.SetLineColor(ROOT.kGreen+3)
            self.Cut2.Draw('same PL')


        self.Title = 'Bump Bonding: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()
        self.ResultData['KeyValueDictPairs']['Mean']['Value'] = round(mean, 2)
        self.ResultData['KeyList'].append('Mean')
        self.ResultData['KeyValueDictPairs']['RMS']['Value'] = round(rms, 2)
        self.ResultData['KeyList'].append('RMS')
        self.ResultData['KeyValueDictPairs']['Threshold']['Value'] = round(thr, 2)
        self.ResultData['KeyList'].append('Threshold')

        if self.Attributes['isDigitalROC']:
            self.ResultData['KeyValueDictPairs']['nSigma']['Value'] = nSigma
            self.ResultData['KeyValueDictPairs']['nBumpBondingProblems']['Value'] = round(nBumpBondingProblems, 0)
            self.ResultData['KeyValueDictPairs']['nBumpBondingProblems2']['Value'] = "{N:1.0f}".format(N=nBumpBondingProblems2)
            self.ResultData['KeyList'].append('nSigma')
            self.ResultData['KeyList'].append('nBumpBondingProblems')
            self.ResultData['KeyList'].append('nBumpBondingProblems2')


