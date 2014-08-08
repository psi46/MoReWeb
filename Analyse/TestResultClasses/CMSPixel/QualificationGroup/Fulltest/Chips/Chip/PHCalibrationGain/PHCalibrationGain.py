# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationGain_TestResult'
        self.NameSingle='PHCalibrationGain'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'



    def PopulateResultData(self):

        #hg
        self.ResultData['Plot']['ROOTObject_hGain'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain

        #hgm
        self.ResultData['Plot']['ROOTObject_hGainMap'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0, self.nCols, self.nRows, 0, self.nRows) # hGainMap

        # hgm
        self.ResultData['Plot']['ROOTObject_hPedestalMap'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0, self.nCols, self.nRows, 0, self.nRows)  # hPedestalMap

        #hp
        self.ResultData['Plot']['ROOTObject_hPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # hPedestal
        self.ResultData['Plot']['ROOTObject_hPedestal'].StatOverflows(True)

        #rp
        self.ResultData['Plot']['ROOTObject_rPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 900, -300., 600.) # rPedestal
        self.ResultData['Plot']['ROOTObject_rPedestal'].StatOverflows(False)

        Parameters = [] # Parameters of Vcal vs. Pulse Height Fit


        Directory = self.RawTestSessionDataPath
        # originally: phCalibrationFit_C
        PHCalibrationFitFileName = "{Directory}/phCalibrationFit_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        PHCalibrationFitFile = open(PHCalibrationFitFileName, "r")
        self.FileHandle = PHCalibrationFitFile #needed in summary

        #PHCalibrationFitFile.seek(2*200) # omit the first 400 bytes

        if PHCalibrationFitFile:
            # for (int i = 0 i < 2 i++) fgets(string, 200, phLinearFile)
            for i in range(4):
                Line = PHCalibrationFitFile.readline() # Omit first four lines
            for Line in PHCalibrationFitFile.readlines():
                    if Line:
                        Parameters = Line.strip().split()
                        # 0.0 0.0 0.249260980545  -24.9957127636  0.0 0.0 Pix  1 13
                        # -->
                        # 0: Parameters[0]
                        # 1: Parameters[1]
                        # 2: Parameters[2]
                        # 3: Parameters[3]
                        # 4: Parameters[4]
                        # 5: Parameters[5]
                        # PIX
                        # column
                        # row
                        # Parameters[0], Parameters[1], Parameters[2], Parameters[3], Parameters[4], Parameters[5], d, a, b = line.strip().split()
                        try:
                            row = int(Parameters[-1])
                            col = int(Parameters[-2])
                            par2 = float(Parameters[2])
                            par3 = float(Parameters[3])
                            if abs(par2) > 1e-10 :  # dead pixels have par2 == 0.
                                Gain = 1. / float(par2)
                                Pedestal = float(par3)
                                i = col
                                j = row
                                if not (i in range(self.nCols)) or not (j in range(self.nRows)):
                                    print 'ERROR', i, j, self.nCols, self.nRows, (i in range(self.nCols)), (j in range(self.nRows))
#                                 print col, row, Gain, Pedestal
                                self.ResultData['Plot']['ROOTObject_hPedestal'].Fill(Pedestal)
                                self.ResultData['Plot']['ROOTObject_hGain'].Fill(Gain)
                                self.ResultData['Plot']['ROOTObject_hGainMap'].SetBinContent(col + 1, row + 1, min(max(0, Gain), 5.5))  # Column, Row, Gain
                                self.ResultData['Plot']['ROOTObject_hPedestalMap'].SetBinContent(col + 1, row + 1, Pedestal)  # Column, Row, Gain

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
            self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().SetTitle("Gain [ADC/Vcal - Par1]");
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


