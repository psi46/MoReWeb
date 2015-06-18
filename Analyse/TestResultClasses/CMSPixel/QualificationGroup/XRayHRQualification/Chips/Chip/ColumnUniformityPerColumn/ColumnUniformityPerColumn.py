# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


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
            rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{:d}'.format(Rate)]
            HitROOTOBjects[Rate] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(),'',self.nCols,0,self.nCols)
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            RealHitrate150 = self.ParentObject.ResultData['SubTestResults']['HitMap_150'].ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
            RealHitrate50 = self.ParentObject.ResultData['SubTestResults']['HitMap_50'].ResultData['KeyValueDictPairs']['RealHitrate']['NumericValue']
            for Column in range(self.nCols):
                HitRate150 = HitROOTOBjects[150].GetBinContent(Column+1)
                HitRate50 = HitROOTOBjects[50].GetBinContent(Column+1)
                if HitRate50 > 0 and RealHitrate50 > 0:
                    ColumnEfficiency = (
                        float(HitRate150)
                        /float(HitRate50)
                        /float(RealHitrate150)
                        *float(RealHitrate50)
                    )
                else:
                    ColumnEfficiency = 0
                self.ResultData['Plot']['ROOTObject'].SetBinContent(Column+1, ColumnEfficiency)

            
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 1.2 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Uniformity");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();
            
            
            
            Fit = self.ResultData['Plot']['ROOTObject'].Fit('pol0','RQ0')
            #mN
            Mean = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParameter(0)
            #sN
            RMS = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParError(0)
            
            
            lineCLow = ROOT.TLine().DrawLine(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_Factor_ColUniformity']*RMS,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_Factor_ColUniformity']*RMS,
            )
            lineCLow.SetLineWidth(2);
            lineCLow.SetLineStyle(2)
            lineCLow.SetLineColor(ROOT.kRed)
            
            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.2f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['mu','sigma']
            

        self.Title = 'Col. Uniformity Ratio: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        self.SaveCanvas()        


