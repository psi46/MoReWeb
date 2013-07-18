# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_ModuleTestGroup_Module_Chips_Chip_PHCalibrationGain_TestResult'
        self.NameSingle='PHCalibrationGain'
        self.Attributes['TestedObjectType'] = 'CMSPixel_ModuleTestGroup_Module_ROC'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        
        #hg
        self.ResultData['Plot']['ROOTObject_hGain'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain
        
        #hgm
        self.ResultData['Plot']['ROOTObject_hGainMap'] = ROOT.TH2D(self.GetUniqueID(), "", 52, 0, 52, 80, 0, 80) # hGainMap
        
        #hp
        self.ResultData['Plot']['ROOTObject_hPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # hPedestal
        self.ResultData['Plot']['ROOTObject_hPedestal'].StatOverflows(True)
    
        #rp
        self.ResultData['Plot']['ROOTObject_rPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # rPedestal
        self.ResultData['Plot']['ROOTObject_rPedestal'].StatOverflows(False)
    
        Parameters = [] # Parameters of Vcal vs. Pulse Height Fit
        
        
        Directory = self.FullTestResultsPath
        # originally: phCalibrationFit_C
        PHCalibrationFitFileName = "{Directory}/phCalibrationFit_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        PHCalibrationFitFile = open(PHCalibrationFitFileName, "r")
        self.FileHandle = PHCalibrationFitFile #needed in summary
        
        #PHCalibrationFitFile.seek(2*200) # omit the first 400 bytes
        
        if PHCalibrationFitFile:
            # for (int i = 0 i < 2 i++) fgets(string, 200, phLinearFile)
            for i in range(4):
                Line = PHCalibrationFitFile.readline() # Omit first four lines
            
            for i in range(52): #Columns
                for j in range(80): #Rows
                    Line = PHCalibrationFitFile.readline()
                    if Line:
                        
                        #Parameters[0], Parameters[1], Parameters[2], Parameters[3], Parameters[4], Parameters[5], d, a, b = line.strip().split()
                        Parameters = Line.strip().split()
                        try:
                            float(Parameters[2])
                            float(Parameters[3])
                            
                            if abs(float(Parameters[2])) > 1e-10 : #dead pixels have par2 == 0.
                                Gain = 1./float(Parameters[2])
                                Pedestal = float(Parameters[3])
                                
                                self.ResultData['Plot']['ROOTObject_hPedestal'].Fill(Pedestal)
                                self.ResultData['Plot']['ROOTObject_hGain'].Fill(Gain)
                                self.ResultData['Plot']['ROOTObject_hGainMap'].SetBinContent(i + 1, j + 1, Gain) # Column, Row, Gain
                            
                        except (ValueError, TypeError, IndexError):
                            pass
                        
            
            
            
            # -- Gain
        
            #mG
            MeanGain = self.ResultData['Plot']['ROOTObject_hGain'].GetMean()
            #sG
            RMSGain = self.ResultData['Plot']['ROOTObject_hGain'].GetRMS()
            #nG
            IntegralGain = self.ResultData['Plot']['ROOTObject_hGain'].Integral(
                self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().GetFirst(), 
                self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().GetLast()
            )
            #nG_entries
            IntegralGain_Entries = self.ResultData['Plot']['ROOTObject_hGain'].GetEntries()
            
            under = self.ResultData['Plot']['ROOTObject_hGain'].GetBinContent(0)
            over = self.ResultData['Plot']['ROOTObject_hGain'].GetBinContent(self.ResultData['Plot']['ROOTObject_hGain'].GetNbinsX()+1)
                
            ROOT.gPad.SetLogy(1)
            
            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetRangeUser(0.5, 5.0*self.ResultData['Plot']['ROOTObject_hGain'].GetMaximum())
            self.ResultData['Plot']['ROOTObject_hGain'].SetLineColor(ROOT.kBlack)
            self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().SetTitle("Gain [ADC/DAC]");
            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetTitle("No. of Entries");
            self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetTitleOffset(1.2);
            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().CenterTitle();
            self.ResultData['Plot']['ROOTObject_hGain'].Draw()
            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTObject_hGain']
            
            
            
            
            self.ResultData['KeyValueDictPairs'] = {
                'N': {
                    'Value':'{0:1.0f}'.format(IntegralGain), 
                    'Label':'N'
                },
                'mu': {
                    'Value':'{0:1.2f}'.format(MeanGain), 
                    'Label':'μ'
                },
                'sigma':{
                    'Value':'{0:1.2f}'.format(RMSGain), 
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
            
            if self.ParentObject.Attributes['ModuleVersion'] == 1:
                self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue)
                self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['Plot']['ROOTObject'].Draw('same')
                self.ResultData['KeyValueDictPairs'].update({
                    'Par1N': {
                        'Value':self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['KeyValueDictPairs']['N']['Value'], 
                        'Label':'Par1 N'
                    },
                    'Par1mu': {
                        'Value':self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['KeyValueDictPairs']['mu']['Value'], 
                        'Label':'Par1 μ'
                    },
                    'Par1sigma':{
                        'Value':self.ParentObject.ResultData['SubTestResults']['PHCalibrationTan'].ResultData['KeyValueDictPairs']['sigma']['Value'], 
                        'Label':'Par1 σ'
                    }
                })
                self.ResultData['KeyList'] += ['Par1N','Par1mu','Par1sigma']
                
            
            if self.SavePlotFile:
                self.Canvas.SaveAs(self.GetPlotFileName())      
            self.ResultData['Plot']['Enabled'] = 1
            self.ResultData['Plot']['Caption'] = 'PH Calibration: Gain (ADC/DAC)'
            self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
            
            
