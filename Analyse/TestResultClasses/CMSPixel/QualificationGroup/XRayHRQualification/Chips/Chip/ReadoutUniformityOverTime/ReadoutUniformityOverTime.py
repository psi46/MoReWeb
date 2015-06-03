# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_ReadoutUniformityOverTime_TestResult'
        self.NameSingle = 'ReadoutUniformityOverTime'
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
                    self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate=self.Attributes['Rate'])],
                    "Xray.hitsVsEvents_Ag_C{ChipNo}_V0".format(ChipNo=ChipNo) 
                )
            )
        
        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("");
            
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 1.2 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Event");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Hits");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();
            
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )
            
            Fit = self.ResultData['Plot']['ROOTObject'].Fit('pol0','RQ0')
            #mN
            Mean = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParameter(0)
            #sN
            RMS = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParError(0)
            #nN
            Integral = self.ResultData['Plot']['ROOTObject'].Integral(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
            )
            
            lineCLow = ROOT.TLine().DrawLine(
                0, Mean-self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetBinCenter(self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()), Mean-self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS,
            )
            lineCLow.SetLineWidth(2);
            lineCLow.SetLineStyle(2)
            lineCLow.SetLineColor(ROOT.kRed)
            
            lineCHigh = ROOT.TLine().DrawLine(
                0, Mean+self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetBinCenter(self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()), Mean+self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS,
            )
            lineCHigh.SetLineWidth(2);
            lineCHigh.SetLineStyle(2)
            lineCHigh.SetLineColor(ROOT.kRed)
            
            self.ResultData['KeyValueDictPairs']['N']['Value'] = '{0:1.0f}'.format(Integral)
            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.0f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMS)

            self.ResultData['KeyList'] += ['N','mu','sigma']
            

        self.Title = 'Read. Unif. over Time {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        self.SaveCanvas()        


