# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import math

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
            'sigma_th':{
                'Value':'{0:1.2f}'.format(-1),
                'Label':'σ_th'
            }
        }
        
    def PopulateResultData(self):
        ChipNo = self.ParentObject.Attributes['ChipNo']

        histogramName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'hitsVsEvents').format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        rootFileHandle = self.ParentObject.ParentObject.ParentObject.Attributes['ROOTFiles']['HRData_{Rate}'.format(Rate = self.Attributes['Rate'])]
        self.ResultData['Plot']['ROOTObject'] = HistoGetter.get_histo(rootFileHandle, histogramName).Clone(self.GetUniqueID())

        if self.ResultData['Plot']['ROOTObject']:
            ROOT.gStyle.SetOptStat(0)
            self.Canvas.Clear()
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, 1.2 * self.ResultData['Plot'][
                'ROOTObject'].GetMaximum())
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Event")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Hits")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw()
            
            
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()-1
            )
            
            #Fit = self.ResultData['Plot']['ROOTObject'].Fit('pol0','RQ0')
            #mN
            #Mean = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParameter(0)
            #sN
            #RMS = self.ResultData['Plot']['ROOTObject'].GetFunction('pol0').GetParError(0)

            FirstBin = self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst()
            LastBin = self.ResultData['Plot']['ROOTObject'].FindLastBinAbove(0)

            # cut away at maximum 5%
            if LastBin < 0.95 * self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast():
                LastBin = int(0.95 * self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast())

            #nN
            Integral = self.ResultData['Plot']['ROOTObject'].Integral(FirstBin, LastBin)

            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange(FirstBin, LastBin)
            Mean = Integral / (LastBin - FirstBin + 1)
            RMS = self.ResultData['Plot']['ROOTObject'].GetRMS()

            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRange()

            RMS_theoretical = math.sqrt(Mean)

            lineCLow = ROOT.TLine().DrawLine(
                0, Mean-self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS_theoretical,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetBinCenter(self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()), Mean-self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS_theoretical,
            )
            lineCLow.SetLineWidth(2);
            lineCLow.SetLineStyle(2)
            lineCLow.SetLineColor(ROOT.kRed)
            
            lineCHigh = ROOT.TLine().DrawLine(
                0, Mean+self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS_theoretical,
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetBinCenter(self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()), Mean+self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_factor_readout_uniformity']*RMS_theoretical,
            )
            lineCHigh.SetLineWidth(2);
            lineCHigh.SetLineStyle(2)
            lineCHigh.SetLineColor(ROOT.kRed)

            self.ResultData['KeyValueDictPairs']['N']['Value'] = '{0:1.0f}'.format(Integral)
            self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.0f}'.format(Mean)
            self.ResultData['KeyValueDictPairs']['sigma_th']['Value'] = '{0:1.2f}'.format(RMS_theoretical)
            self.ResultData['KeyList'] += ['N','mu','sigma_th']

        self.Title = 'Read. Unif. over Time {Rate}: C{ChipNo}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'],Rate=self.Attributes['Rate'])
        self.SaveCanvas()        


