# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_SCurveWidths_TestResult'
        self.NameSingle='SCurveWidths'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        
        #   // -- sCurve width and noise level
        
        self.ParentObject.ParentObject.FileHandle.Get("AddressLevels_C{ChipNo}".format(ChipNo=self.ParentObject.Attributes['ChipNo']) )
        
        #hw
        self.ResultData['Plot']['ROOTObject'] =ROOT.TH1D(self.GetUniqueID(), "", 100, 0., 600.) # hw
        self.ResultData['Plot']['ROOTObject_hd'] =ROOT.TH1D(self.GetUniqueID(), "", 100, 0., 600.) #Noise in unbonded pixel (not displayed) # hd
        self.ResultData['Plot']['ROOTObject_ht'] = ROOT.TH2D(self.GetUniqueID(), "", 52, 0., 52., 80, 0., 80.) # ht
        isDigitalROC = False
        if self.ParentObject.ParentObject.FileHandle.Get("vcals_xtalk_C{ChipNo}".format(ChipNo=self.ParentObject.Attributes['ChipNo'])):
#            print 'SCurve Analog module'
            self.ResultData['Plot']['ROOTObject_h2'] = ROOT.TH2D(
                                                             self.ParentObject.ParentObject.FileHandle.Get("vcals_xtalk_C{ChipNo}".format(ChipNo=self.ParentObject.Attributes['ChipNo']) )
                                                             )
        else:
#            print 'SCurve Digital module'
            isDigitalROC = True
            self.ResultData['Plot']['ROOTObject_h2'] = ROOT.TH2D(
                                                             self.ParentObject.ParentObject.FileHandle.Get("BumpBondMap_C{ChipNo}".format(ChipNo=self.ParentObject.Attributes['ChipNo']) )
                                                             )
        
        Directory = self.FullTestResultsPath
        SCurveFileName = "{Directory}/SCurve_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        SCurveFile = open(SCurveFileName, "r")
        
        self.FileHandle = SCurveFile # needed in summary
        
        if SCurveFile:
            #Omit the first two lines
            Line = SCurveFile.readline()
            Line = SCurveFile.readline()
            
            for column in range(52): #Columns
                for row in range(80): #Rows
                    Line = SCurveFile.readline()
                    if Line:
                        LineArray = Line.strip().split()
                        Threshold = float(LineArray[0])
                        Sign = float(LineArray[1])
                        #Threshold, Sign, SomeString, a, b = Line.strip().split()
                        
                        self.ResultData['Plot']['ROOTObject'].Fill(Sign)
                        Threshold = Threshold / self.TestResultEnvironmentObject.GradingParameters['StandardADC2ElectronConversionFactor']
                        self.ResultData['Plot']['ROOTObject_ht'].SetBinContent(column+1, row+1, Threshold)
                        if not isDigitalROC and self.ResultData['Plot']['ROOTObject_h2'].GetBinContent(column+1, row+1) >= self.TestResultEnvironmentObject.GradingParameters['minThrDiff']:
                            self.ResultData['Plot']['ROOTObject_hd'].Fill(Sign)
                        elif isDigitalROC and self.ResultData['Plot']['ROOTObject_h2'].GetBinContent(column+1, row+1) <= self.TestResultEnvironmentObject.GradingParameters['BumpBondThr']:
                            self.ResultData['Plot']['ROOTObject_hd'].Fill(Sign)
            
            
        self.ResultData['HiddenData']['htmax'] = 255.;
        self.ResultData['HiddenData']['htmin'] = 0.
    
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
                
            
        self.ResultData['KeyValueDictPairs'] = {
            'N': {
                'Value':'{0:1.0f}'.format(IntegralSCurve), 
                'Label':'N'
            },
            'mu': {
                'Value':'{0:1.2f}'.format(MeanSCurve), 
                'Label':'μ'
            },
            'sigma':{
                'Value':'{0:1.2f}'.format(RMSSCurve), 
                'Label':'σ'
            }
        }
        
        self.ResultData['KeyList'] = ['N','mu','sigma']
        if under:
            self.ResultData['KeyValueDictPairs']['under'] = {'Value':'{0:1.2f}'.format(under), 'Label':'<='}
            self.ResultData['KeyList'].append('under')
        if over:
            self.ResultData['KeyValueDictPairs']['over'] = {'Value':'{0:1.2f}'.format(over), 'Label':'>='}
            self.ResultData['KeyList'].append('over')

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())      
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['Caption'] = 'S-Curve widths: Noise (e^{-})'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
