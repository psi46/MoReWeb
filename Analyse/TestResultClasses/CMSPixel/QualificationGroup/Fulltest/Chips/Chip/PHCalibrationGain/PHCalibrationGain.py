# -*- coding: utf-8 -*-
import warnings
import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_PHCalibrationGain_TestResult'
        self.NameSingle = 'PHCalibrationGain'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.verbose = False
        self.GainDefectsList = set([])
        self.ResultData['KeyValueDictPairs']['GainDefects'] = {'Value': None, 'Label': 'Gain defects'}

    def fill_histograms(self):
        Directory = self.RawTestSessionDataPath
        try:
            ThresholdDefectsList = self.ParentObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['KeyValueDictPairs']['TrimProblems']['Value']
        except:
            ThresholdDefectsList = set([])

        # originally: phCalibrationFit_C
        chip = self.ParentObject.Attributes['ChipNo']
        PHCalibrationFitFileName = "{Directory}/phCalibrationFit_C{ChipNo}.dat".format(Directory=Directory,
                                                                                       ChipNo=chip)
        PHCalibrationFitFile = open(PHCalibrationFitFileName, "r")
        self.FileHandle = PHCalibrationFitFile  # needed in summary

        if not PHCalibrationFitFile:
            warnings.warn('Cannot find File')
            return False

        n_lines = 0
        for i in range(3):
            PHCalibrationFitFile.readline()  # Omit first four lines

        n_dead_pixels = 0
        n_errors = 0
        n_warnings = 0
        for Line in PHCalibrationFitFile.readlines():
            n_lines += 1
            if Line:
                try:
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
                    row = int(Parameters[-1])
                    col = int(Parameters[-2])
                    par2 = float(Parameters[2])
                    par3 = float(Parameters[3])
                    if self.verbose:
                        print '%2d %2d: %5f %5f '%(row,col,par2,par3)

                    if abs(par2) < 1e-10:  # dead pixels have par2 == 0.
                        n_dead_pixels += 1
                    else:
                        gain = 1. / float(par2)  # gain in Vcal/adc
                        pedestal = float(par3) * gain  # Pedestal in Vcal / vcal offset : units: adc * vcal/adc = vcal
                        if not (0 <= row < self.nRows and 0 <= col < self.nCols):
                            warnings.warn(
                                'PHCalibrationGain: pixel address out of bounds: {col}/{row}'.format(col=col,
                                                                                                     row=row))
                            n_warnings += 1
                            continue
                        if self.isPROC:
                            ChannelNumber = (col % 2) + 2*(row % 2)
                            self.ResultData['Plot']['ROOTObject_hPedestal_c%d'%ChannelNumber].Fill(pedestal)
                            self.ResultData['Plot']['ROOTObject_hGain_c%d'%ChannelNumber].Fill(gain)

                        self.ResultData['Plot']['ROOTObject_hPedestal'].Fill(pedestal)
                        self.ResultData['Plot']['ROOTObject_hGain'].Fill(gain)

                        self.ResultData['Plot']['ROOTObject_hGainMap'].SetBinContent(col + 1, row + 1, gain)
                        self.ResultData['Plot']['ROOTObject_hPedestalMap'].SetBinContent(col + 1, row + 1, pedestal)
                        if gain > self.TestResultEnvironmentObject.GradingParameters['gainMax'] or gain < self.TestResultEnvironmentObject.GradingParameters['gainMin']:
                            if (chip, col, row) not in ThresholdDefectsList:
                                self.GainDefectsList.add((chip, col, row))

                except (ValueError, TypeError, IndexError):
                    n_errors += 1
                    pass
        if self.verbose:
            print 'Filled {pixels} to histogram'.format(pixels=self.ResultData['Plot']['ROOTObject_hGain'].GetEntries()),n_dead_pixels,n_errors,n_warnings,n_lines
        return True

    def PopulateResultData(self):

        # hg
        self.ResultData['Plot']['ROOTObject_hGain'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain

        if self.isPROC:
            #  pixel cluster channels todo:check with PSI for numbering
            #  2 3
            #  0 1
            self.ResultData['Plot']['ROOTObject_hGain_c0'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain channel 0
            self.ResultData['Plot']['ROOTObject_hGain_c1'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain channel 1
            self.ResultData['Plot']['ROOTObject_hGain_c2'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain channel 2
            self.ResultData['Plot']['ROOTObject_hGain_c3'] = ROOT.TH1D(self.GetUniqueID(), "", 300, -2.0, 5.5)  # hGain channel 3

        # hgm
        self.ResultData['Plot']['ROOTObject_hGainMap'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0, self.nCols,
                                                                   self.nRows, 0, self.nRows)  # hGainMap

        # hgm
        self.ResultData['Plot']['ROOTObject_hPedestalMap'] = ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0,
                                                                       self.nCols, self.nRows, 0,
                                                                       self.nRows)  # hPedestalMap

        # hp
        self.ResultData['Plot']['ROOTObject_hPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 2100, -1500., 600.)  # hPedestal
        self.ResultData['Plot']['ROOTObject_hPedestal'].StatOverflows(True)

        if self.isPROC:
            self.ResultData['Plot']['ROOTObject_hPedestal_c0'] = ROOT.TH1D(self.GetUniqueID(), "", 2100, -1500., 600.)  # hPedestal channel 0
            self.ResultData['Plot']['ROOTObject_hPedestal_c1'] = ROOT.TH1D(self.GetUniqueID(), "", 2100, -1500., 600.)  # hPedestal channel 1
            self.ResultData['Plot']['ROOTObject_hPedestal_c2'] = ROOT.TH1D(self.GetUniqueID(), "", 2100, -1500., 600.)  # hPedestal channel 2
            self.ResultData['Plot']['ROOTObject_hPedestal_c3'] = ROOT.TH1D(self.GetUniqueID(), "", 2100, -1500., 600.)  # hPedestal channel 3

        # rp
        self.ResultData['Plot']['ROOTObject_rPedestal'] = ROOT.TH1D(self.GetUniqueID(), "", 2100, -1500.,
                                                                    600.)  # rPedestal
        self.ResultData['Plot']['ROOTObject_rPedestal'].StatOverflows(False)

        if self.fill_histograms():
            # -- Gain
            # mG
            MeanGain = self.ResultData['Plot']['ROOTObject_hGain'].GetMean()
            # sG
            RMSGain = self.ResultData['Plot']['ROOTObject_hGain'].GetRMS()
            # nG
            IntegralGain = self.ResultData['Plot']['ROOTObject_hGain'].Integral(
                self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().GetFirst(),
                self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().GetLast()
            )
            # nG_entries
            # IntegralGain_Entries = self.ResultData['Plot']['ROOTObject_hGain'].GetEntries()

            under = self.ResultData['Plot']['ROOTObject_hGain'].GetBinContent(0)
            over = self.ResultData['Plot']['ROOTObject_hGain'].GetBinContent(
                self.ResultData['Plot']['ROOTObject_hGain'].GetNbinsX() + 1)

            ROOT.gPad.SetLogy(1)

            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetRangeUser(0.5, 5.0 * self.ResultData['Plot'][
                'ROOTObject_hGain'].GetMaximum())
            self.ResultData['Plot']['ROOTObject_hGain'].SetLineColor(ROOT.kBlack)
            self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().SetTitle("Gain [Vcal/ADC]")
            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetTitle("No. of Entries")
            self.ResultData['Plot']['ROOTObject_hGain'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().SetTitleOffset(1.2)
            self.ResultData['Plot']['ROOTObject_hGain'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject_hGain'].Draw()
            self.ResultData['Plot']['ROOTObject'] = self.ResultData['Plot']['ROOTObject_hGain']

            self.ResultData['KeyValueDictPairs'] = {
                'N': {
                    'Value': '{0:1.0f}'.format(IntegralGain),
                    'Label': 'N'
                },
                'mu': {
                    'Value': '{0:1.2f}'.format(MeanGain),
                    'Label': 'μ'
                },
                'sigma': {
                    'Value': '{0:1.2f}'.format(RMSGain),
                    'Label': 'RMS'
                },
                'GainDefects': {
                    'Value': self.GainDefectsList,
                    'Label': 'Gain defects'
                },
                'NGainDefects': {
                    'Value': '{0:1.0f}'.format(len(self.GainDefectsList)),
                    'Label': '# Gain defects'
                },

            }
            self.ResultData['KeyList'] = ['N', 'mu', 'sigma', 'NGainDefects']
            if under:
                self.ResultData['KeyValueDictPairs']['under'] = {'Value': '{0:1.2f}'.format(under), 'Label': '<='}
                self.ResultData['KeyList'].append('under')
            if over:
                self.ResultData['KeyValueDictPairs']['over'] = {'Value': '{0:1.2f}'.format(over), 'Label': '>='}
                self.ResultData['KeyList'].append('over')

            self.ResultData['Plot']['ROOTObject_LowEdge'] = ROOT.TCutG('lLower', 2)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetPoint(0, self.TestResultEnvironmentObject.GradingParameters['gainMin'], -1e6)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetPoint(1, self.TestResultEnvironmentObject.GradingParameters['gainMin'], +1e6)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetLineColor(ROOT.kRed)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetLineStyle(2)
            self.ResultData['Plot']['ROOTObject_LowEdge'].Draw('same')

            self.ResultData['Plot']['ROOTObject_UpEdge'] = ROOT.TCutG('lUpper', 2)
            self.ResultData['Plot']['ROOTObject_UpEdge'].SetPoint(0, self.TestResultEnvironmentObject.GradingParameters['gainMax'], -1e6)
            self.ResultData['Plot']['ROOTObject_UpEdge'].SetPoint(1, self.TestResultEnvironmentObject.GradingParameters['gainMax'], +1e6)
            self.ResultData['Plot']['ROOTObject_UpEdge'].SetLineColor(ROOT.kRed)
            self.ResultData['Plot']['ROOTObject_UpEdge'].SetLineStyle(2)
            self.ResultData['Plot']['ROOTObject_UpEdge'].Draw('same')

            self.SaveCanvas()
            self.ResultData['Plot']['Caption'] = 'PH Calibration: Gain (Vcal/ADC)'
            ROOT.gPad.SetLogy(0)

