# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_ColumnUniformityEventsPerColumn_TestResult'
        self.NameSingle = 'ColumnUniformityEventsPerColumn'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['HiddenData']['EventBins'] = 0
        self.ResultData['KeyValueDictPairs'] = {
            'mu': {
                'Value':'{0:1.2f}'.format(-1),
                'Label':'μ'
            },
            'sigma':{
                'Value':'{0:1.2f}'.format(-1),
                'Label':'fit error of μ'
            }
        }

    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']
        HitsVsEventsROOTObjects = {}
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        EventBins = 0
        EventMin = 0
        EventMax = 0
        Rate = self.Attributes['Rate']

        histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'hitsVsEvtCol').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=Rate)]
        self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        self.ResultData['HiddenData']['EventBins'] = max(
            self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast(),EventBins)

        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("")

            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Event")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Column")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')

            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )

            #why a fit anyway...
            FitPol0 = ROOT.TF1("GaussFitFunction", "pol0")
            self.ResultData['Plot']['ROOTObject'].Fit(FitPol0,'RQ0')

            Mean = -1
            RMS = -1
            if FitPol0:
                Mean = FitPol0.GetParameter(0)
                RMS = FitPol0.GetParError(0) # not rms but par0 error...

            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
            )

            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.2f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['mu','sigma']

            ROOT.gPad.Update()

        self.Title = 'Col. Uniformity per Event: C{ChipNo} {Rate}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'], Rate=self.Attributes['Rate'])
        self.SaveCanvas()


