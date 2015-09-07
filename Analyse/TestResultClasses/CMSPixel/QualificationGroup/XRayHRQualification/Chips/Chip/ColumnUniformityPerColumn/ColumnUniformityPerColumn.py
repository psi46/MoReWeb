# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_ColumnUniformityPerColumn_TestResult'
        self.NameSingle = 'ColumnUniformityPerColumn'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['KeyValueDictPairs'] = {
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
        HitROOTOBjects = {}

        histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'hitsVsColumn').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']['HRData']
        for Rate in Rates:
            rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=Rate)]
            HitROOTOBjects[Rate] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(),'',self.nCols,0,self.nCols)
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            HitRateHigh = 150
            HitRateLow = 50

            if not 'HitMap_{Rate}'.format(Rate=HitRateHigh) in self.ParentObject.ResultData['SubTestResults']:
                HitRateHigh = max(Rates)

            if not 'HitMap_{Rate}'.format(Rate=HitRateLow) in self.ParentObject.ResultData['SubTestResults']:
                HitRateLow = min(Rates)

            RealHitrateHigh = self.ParentObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=HitRateHigh)].ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
            RealHitrateLow = self.ParentObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=HitRateLow)].ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
            for Column in range(self.nCols):
                NumHitsHigh = HitROOTOBjects[HitRateHigh].GetBinContent(Column+1)
                NumHitsLow = HitROOTOBjects[HitRateLow].GetBinContent(Column+1)
                if HitRateLow > 0 and RealHitrateLow > 0 and RealHitrateHigh > 0 and NumHitsLow > 0:
                    ColumnUniformity = (
                        float(NumHitsHigh)
                        /float(NumHitsLow)
                        /float(RealHitrateHigh)
                        *float(RealHitrateLow)
                    )
                else:
                    ColumnUniformity = 0
                self.ResultData['Plot']['ROOTObject'].SetBinContent(Column+1, ColumnUniformity)

            self.ResultData['Plot']['ROOTObject'].SetTitle("");

            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 1.2 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Uniformity")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].Draw()

            ColumnRatios = array.array('d', [])
            for i in range(1, self.ResultData['Plot']['ROOTObject'].GetNbinsX()+1):
                ColumnRatios.append(self.ResultData['Plot']['ROOTObject'].GetBinContent(i))

            Mean = ROOT.TMath.Mean(len(ColumnRatios), ColumnRatios)
            RMS = ROOT.TMath.RMS(len(ColumnRatios), ColumnRatios)

            lineCLow = ROOT.TLine().DrawLine(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_low'],
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_low'],
            )
            lineCLow.SetLineWidth(2)
            lineCLow.SetLineStyle(2)
            lineCLow.SetLineColor(ROOT.kRed)

            lineCHigh = ROOT.TLine().DrawLine(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high'],
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high'],
            )
            lineCHigh.SetLineWidth(2)
            lineCHigh.SetLineStyle(2)
            lineCHigh.SetLineColor(ROOT.kRed)

            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 1.05*self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high'])

            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.2f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['mu','sigma']

        self.Title = 'Col. Uniformity Ratio: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        


