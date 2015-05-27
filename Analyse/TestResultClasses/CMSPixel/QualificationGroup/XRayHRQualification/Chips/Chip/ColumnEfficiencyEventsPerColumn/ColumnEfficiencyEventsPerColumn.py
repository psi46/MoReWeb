# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_ReadoutUniformityOverTime_TestResult'
        self.NameSingle = 'ReadoutUniformityOverTime'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_XRayHRQualification_ROC'
        self.ResultData['HiddenData']['EventBins'] = 0
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
        HitsVsEventsROOTObjects = {}
        Rates = self.ParentObject.ParentObject.ParentObject.Attributes['Rates']
        EventBins = 0
        EventMin = 0
        EventMax = 0
        for Rate in Rates:
            HitsVsEventsROOTObjects[Rate] = (
                HistoGetter.get_histo(
                        self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{:d}'.format(Rate)],
                        "Xray.hitsVsEvtCol_Ag_C{ChipNo}_V0".format(ChipNo=ChipNo) 
                    )
                )
            EventMin = min(HitsVsEventsROOTObjects[Rate].GetXaxis().GetBinCenter(HitsVsEventsROOTObjects[Rate].GetXaxis().GetFirst()),EventMin)
            EventMax = max(HitsVsEventsROOTObjects[Rate].GetXaxis().GetBinCenter(HitsVsEventsROOTObjects[Rate].GetXaxis().GetLast()),EventMax)
            EventBins = max(HitsVsEventsROOTObjects[Rate].GetXaxis().GetLast(),EventBins)
        self.ResultData['HiddenData']['EventBins'] = EventBins
        ColumnEfficiencyPerColumnTestResultObject = self.ParentObject.ResultData['SubTestResults']['ColumnEfficiencyPerColumn']
        
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(),'',EventBins, EventMin, EventMax, self.nCols, 0,self.nCols)
        
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            RealHitrate150 = self.ParentObject.ResultData['SubTestResults']['HitMap_150'].ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
            RealHitrate50 = self.ParentObject.ResultData['SubTestResults']['HitMap_50'].ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
            
            
            for Column in range(self.nCols):
                ColumnEfficiency = ColumnEfficiencyPerColumnTestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(Column+1)
                for EventBin in range(EventBins):
                    Hits150 = HitsVsEventsROOTObjects[150].GetBinContent(EventBin+1,Column+1)
                    Hits50 = HitsVsEventsROOTObjects[50].GetBinContent(EventBin+1,Column+1)
                    if Hits50>0 and RealHitrate50>0:
                        ColumnEfficiencyPerEvent = (
                            float(Hits150)
                            /float(Hits50)
                            *float(RealHitrate150)
                            /float(RealHitrate50)
                        )
                    else:
                        ColumnEfficiencyPerEvent = -1
                    self.ResultData['Plot']['ROOTObject'].SetBinContent(EventBin+1,Column+1,ColumnEfficiencyPerEvent)
                    
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Event");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Column");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw('colz');
            
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )
            
            Fit = self.ResultData['Plot']['ROOTObject'].Fit('pol0','RQ0')
            #mN
            Mean = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParameter(0)
            #sN
            RMS = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParError(0)
            
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
            )
            
            
            
            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.2f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['mu','sigma']
            

        self.Title = 'Col. Eff. per Event: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        


