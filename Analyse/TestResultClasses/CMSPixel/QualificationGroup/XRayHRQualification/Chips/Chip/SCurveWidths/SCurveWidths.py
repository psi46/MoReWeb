# -*- coding: utf-8 -*-
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_Chips_Chip_SCurveWidths_TestResult'
        self.NameSingle='SCurveWidths'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.ResultData['KeyValueDictPairs'] = {
            'N': {
                'Value':'{0:1.0f}'.format(-1),
                'Label':'N'
            },
            'mu': {
                'Value':'{0:1.2f}'.format(-999),
                'Label':'μ'
            },
            'sigma':{
                'Value':'{0:1.2f}'.format(-1),
                'Label':'σ'
            }
        }

        self.ResultData['HiddenData']['htmax'] = 255.;
        self.ResultData['HiddenData']['htmin'] = 0.
        self.ResultData['HiddenData']['NumberOfNoisyPixels'] = 0
        self.ResultData['HiddenData']['ListOfNoisyPixels'] = []

    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(1)
        ChipNo=self.ParentObject.Attributes['ChipNo']
        
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", 100, 0., 600.) # hw
        self.ResultData['Plot']['ROOTObject_hd'] =ROOT.TH1D(self.GetUniqueID(), "", 100, 0., 600.) #Noise in unbonded pixel (not displayed) # hd
        self.ResultData['Plot']['ROOTObject_ht'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows) # ht
        
        Rate = self.Attributes['Rate']
        Directory = self.ParentObject.ParentObject.ParentObject.Attributes['SCurvePaths']['HRSCurves_{:d}'.format(Rate)]
        SCurveBaseName = self.ParentObject.ParentObject.ParentObject.ParentObject.HistoDict.get('HighRate', 'SCurveBaseName')
        SCurveFileName = SCurveBaseName.format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        SCurveFile = open(SCurveFileName, "r")

        self.FileHandle = SCurveFile # needed in summary

        if not SCurveFile:
            raise Exception('Cannot find SCurveFile "%s"'%SCurveFileName)
        else:
            #Omit the first line
            #print 'read file',SCurveFileName
            Line = SCurveFile.readline()

            for column in range(self.nCols): #Columns
                for row in range(self.nRows): #Rows
                    Line = SCurveFile.readline()
                    if Line:
                        LineArray = Line.strip().split()
                        Threshold = float(LineArray[0])
                        Width = float(LineArray[1])
                        
                        self.ResultData['Plot']['ROOTObject'].Fill(Width)
                        Threshold = Threshold / self.TestResultEnvironmentObject.GradingParameters['StandardVcal2ElectronConversionFactor']
                        self.ResultData['Plot']['ROOTObject_ht'].SetBinContent(column+1, row+1, Threshold)
                        self.ResultData['Plot']['ROOTObject_hd'].Fill(Width)
                        if Threshold > self.TestResultEnvironmentObject.GradingParameters['XRayHighRate_SCurve_Noise_Threshold']:
                            self.ResultData['HiddenData']['NumberOfNoisyPixels'] += 1
                            self.ResultData['HiddenData']['ListOfNoisyPixels'].append((ChipNo, column, row))


        if self.ResultData['Plot']['ROOTObject_ht'].GetMaximum() < self.ResultData['HiddenData']['htmax']:
            self.ResultData['HiddenData']['htmax'] = self.ResultData['Plot']['ROOTObject_ht'].GetMaximum();

        if self.ResultData['Plot']['ROOTObject_ht'].GetMinimum() > self.ResultData['HiddenData']['htmin'] :
            self.ResultData['HiddenData']['htmin'] = self.ResultData['Plot']['ROOTObject_ht'].GetMinimum();

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Noise (e^{-})");
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject'].Draw();


        #mN
        MeanSCurve = self.ResultData['Plot']['ROOTObject'].GetMean()
        #sN
        RMSSCurve = self.ResultData['Plot']['ROOTObject'].GetRMS()
        #nN
        IntegralSCurve = self.ResultData['Plot']['ROOTObject'].Integral(
            self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(),
            self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
        )
        #nN_entries
        IntegralSCurve_Entries = self.ResultData['Plot']['ROOTObject'].GetEntries()

        under = self.ResultData['Plot']['ROOTObject'].GetBinContent(0)
        over = self.ResultData['Plot']['ROOTObject'].GetBinContent(self.ResultData['Plot']['ROOTObject_hd'].GetNbinsX()+1)

        self.ResultData['KeyValueDictPairs']['N']['Value'] = '{0:1.0f}'.format(IntegralSCurve)
        self.ResultData['KeyValueDictPairs']['mu']['Value'] = '{0:1.2f}'.format(MeanSCurve)
        self.ResultData['KeyValueDictPairs']['sigma']['Value'] = '{0:1.2f}'.format(RMSSCurve)

        self.ResultData['KeyList'] = ['N','mu','sigma']
        if under:
            self.ResultData['KeyValueDictPairs']['under'] = {'Value':'{0:1.2f}'.format(under), 'Label':'<='}
            self.ResultData['KeyList'].append('under')
        if over:
            self.ResultData['KeyValueDictPairs']['over'] = {'Value':'{0:1.2f}'.format(over), 'Label':'>='}
            self.ResultData['KeyList'].append('over')

        self.Title = 'S-Curve widths: Noise (e^{{-}}) C{ChipNo} {Rate}'.format(ChipNo=self.ParentObject.Attributes['ChipNo'], Rate=self.Attributes['Rate'])
        self.SaveCanvas()        