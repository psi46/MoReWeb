# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


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
        self.ResultData['Plot']['ROOTObject'] = (
            HistoGetter.get_histo(
                    self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{:d}'.format(self.Attributes['Rate'])],
                    "Xray.hitsVsColumn_Ag_C{ChipNo}_V0".format(ChipNo=ChipNo) 
                )
            )
        
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 1.2 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Hits");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();
            
            
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst()+1,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )
            Fit = self.ResultData['Plot']['ROOTObject'].Fit('pol0','RQ0')
            #mN
            Mean = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParameter(0)
            #sN
            RMS = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParError(0)
            #nN
            Integral = self.ResultData['Plot']['ROOTObject'].Integral(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst()+1,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
            )
            
            lineCLow = ROOT.TLine().DrawLine(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_low']*Mean,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_low']*Mean,
            )
            lineCLow.SetLineWidth(2);
            lineCLow.SetLineStyle(2)
            lineCLow.SetLineColor(ROOT.kRed)
            
            lineCHigh = ROOT.TLine().DrawLine(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high']*Mean,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast(), self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_dcol_uniformity_high']*Mean,
            )
            lineCHigh.SetLineWidth(2);
            lineCHigh.SetLineStyle(2)
            lineCHigh.SetLineColor(ROOT.kRed)
            
            self.ResultData['KeyValueDictPairs']['N']['Value'] = '{0:1.0f}'.format(Integral)
            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.0f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['N','mu','sigma']
            

        self.Title = 'Col. Read. Unif. {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        self.SaveCanvas()        


