# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationTan_TestResult'
        self.NameSingle = 'PHCalibrationTan'
        self.Show = False
        self.Par1DefectsList = set()
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        

        
    def PopulateResultData(self):
        #PHCalibrationTan = Parameter1
        ChipNo=self.ParentObject.Attributes['ChipNo']
        #hPar1
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", 350, -1., 6.)  # par1
        Directory = self.RawTestSessionDataPath
        
        PHCalibrationFitTanFileName = "{Directory}/phCalibrationFitTan_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        try:
            PHCalibrationFitTanFile = open(PHCalibrationFitTanFileName, "r")
        except IOError:
            raise  IOError("cannot open %s"%PHCalibrationFitTanFileName)
        self.FileHandle = PHCalibrationFitTanFile #needed in summary
        
        #SCurveFile.seek(2*200) # omit the first 400 bytes

        try:
            DeadPixelList = self.ParentObject.ResultData['SubTestResults']['PixelMap'].ResultData['KeyValueDictPairs']['DeadPixels']['Value']
        except:
            DeadPixelList = set([])

        par1Min = self.TestResultEnvironmentObject.GradingParameters['par1Min']
        par1Max = self.TestResultEnvironmentObject.GradingParameters['par1Max']

        if PHCalibrationFitTanFile:
            
            # for (int i = 0 i < 2 i++) fgets(string, 200, phLinearFile)
            for i in range(3):
                PHCalibrationFitTanFile.readline() #Omit first three lines
            
            for col in range(self.nCols):
                for row in range(self.nRows):
                    Line = PHCalibrationFitTanFile.readline()
                    if Line:
                        LineArray = Line.strip().split()
                        try:
                            par1 = float(LineArray[1])
                            if (ChipNo, col, row) not in DeadPixelList:
                                self.ResultData['Plot']['ROOTObject'].Fill(par1)

                                # parameter 1 defects
                                if par1 > par1Max or par1 < par1Min:
                                    self.Par1DefectsList.add((ChipNo, col, row))

                        except (ValueError, TypeError, IndexError):
                            pass
                    
            
            # -- Parameter1
        
            #mPar1
            MeanPar1 = self.ResultData['Plot']['ROOTObject'].GetMean()
            #sPar1
            RMSPar1 = self.ResultData['Plot']['ROOTObject'].GetRMS()
            #nPar1
            IntegralPar1 = self.ResultData['Plot']['ROOTObject'].Integral(
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetFirst(), 
                self.ResultData['Plot']['ROOTObject'].GetXaxis().GetLast()
            )
            #nPar1_entries
            IntegralPar1_Entries = self.ResultData['Plot']['ROOTObject'].GetEntries()
            
            under = self.ResultData['Plot']['ROOTObject'].GetBinContent(0)
            over = self.ResultData['Plot']['ROOTObject'].GetBinContent(self.ResultData['Plot']['ROOTObject'].GetNbinsX()+1)
                
            self.ResultData['KeyValueDictPairs'] = {
                'N': {
                    'Value':'{0:1.0f}'.format(IntegralPar1), 
                    'Label':'N'
                },
                'mu': {
                    'Value':'{0:1.2f}'.format(MeanPar1), 
                    'Label':'μ'
                },
                'sigma':{
                    'Value':'{0:1.2f}'.format(RMSPar1), 
                    'Label':'RMS'
                },
                'Par1Defects':{
                    'Value': self.Par1DefectsList,
                    'Label':'Par1 defects'
                },
                'NPar1Defects':{
                    'Value': '{0:1.0f}'.format(len(self.Par1DefectsList)),
                    'Label':'# Par1 defects'
                },
            }
            self.ResultData['KeyList'] = ['N','mu','sigma','NPar1Defects']
            if under:
                self.ResultData['KeyValueDictPairs']['under'] = {'Value':'{0:1.2f}'.format(under), 'Label':'<='}
                self.ResultData['KeyList'].append('under')
            if over:
                self.ResultData['KeyValueDictPairs']['over'] = {'Value':'{0:1.2f}'.format(over), 'Label':'>='}
                self.ResultData['KeyList'].append('over')
