# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import array

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_ColumnReadoutUniformity_TestResult'
        self.NameSingle = 'ColumnReadoutUniformity'
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

        histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'hitsVsColumn').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=self.Attributes['Rate'])]
        self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("");

            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 1.2 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Hits")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw()

            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst()+1,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )

            ColumnHits = array.array('d', [])
            for i in range(1, self.ResultData['Plot']['ROOTObject'].GetNbinsX()+1):
                ColumnHits.append(self.ResultData['Plot']['ROOTObject'].GetBinContent(i))

            Mean = ROOT.TMath.Mean(len(ColumnHits), ColumnHits)
            RMS = ROOT.TMath.RMS(len(ColumnHits), ColumnHits)

            Integral = self.ResultData['Plot']['ROOTObject'].Integral(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst()+1,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )

            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
            )

            self.ResultData['KeyValueDictPairs']['N']['Value'] = '{0:1.0f}'.format(Integral)
            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.0f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['N','mu','sigma']

        self.Title = 'Col. Read. Unif. {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        self.SaveCanvas()


