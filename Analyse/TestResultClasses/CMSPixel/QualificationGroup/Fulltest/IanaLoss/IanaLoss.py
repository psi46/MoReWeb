# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'IanaLoss'
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.ResultData['KeyValueDictPairs'] = {
            'IanaLossProblems': {
                'Value': '-',
                'Label': 'Iana problems',
            },
            'Mean': {
                'Value': '{0:1.2f}'.format(0),
                'Label': 'mean'
            },
            'Min': {
                'Value': '{0:1.2f}'.format(0),
                'Label': 'min'
            },
            'Max': {
                'Value': '{0:1.2f}'.format(0),
                'Label': 'max'
            },
            'NROCsNotProgrammable': {
                'Value': '0',
                'Label': 'ROCs not programmable',
            },
        }
        self.ResultData['KeyList'] = ['IanaLossProblems', 'Mean', 'Min', 'Max', 'NROCsNotProgrammable']
        self.ResultData['HiddenData']['IanaLossProblems'] = False
        self.ResultData['HiddenData']['ROCsNotProgrammable'] = []

    def PopulateResultData(self):

        ROOT.gStyle.SetOptStat(0)
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

        NChips = self.ParentObject.Attributes['NumberOfChips']
        StartChip = self.ParentObject.Attributes['StartChip']
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), '', NChips, StartChip, StartChip + NChips)

        # read values from logfile
        #  format:
        #  [14:56:48.291]     INFO: i(loss) [mA/ROC]:     16.1  16.1  15.3  ->14.5<-  ->12.9<-  ->12.1<-  ->12.1<-  ->11.3<-  ->9.6<-  ->10.4<-  ->12.1<-  ->12.9<-  ->13.7<-  15.3  16.1  16.1
        IanaLossPerRoc = None
        IanaLossProblems = False
        if self.ParentObject.logfilePath and os.path.isfile(self.ParentObject.logfilePath):
            with open(self.ParentObject.logfilePath, 'r') as logfile:
                for line in logfile:
                    Keyword = 'i(loss) [mA/ROC]:'
                    if Keyword in line:
                        splitPos = line.find(Keyword)
                        if splitPos >=0:
                            IanaLossString = line[splitPos + len(Keyword):]
                            if '->' in IanaLossString and '<-' in IanaLossString:
                                IanaLossProblems = True
                            IanaLossPerRoc = [float(x.replace('->', '').replace('<-', '').strip()) for x in IanaLossString.strip().split(' ') if len(x.replace('->', '').replace('<-', '').strip()) > 0]
                            break

        # check if ROCs are not programmable
        try:
            HistogramName = self.ParentObject.HistoDict.get('Pretest', 'ProgramROC')
            ProgramROCHistogram = HistoGetter.get_histo(self.ParentObject.FileHandle, HistogramName)
        except Exception as e:
            print "WARNING: program ROC histogram not found!"
            ProgramROCHistogram = None

        if ProgramROCHistogram:
            NBins = ProgramROCHistogram.GetXaxis().GetNbins()
            for i in range(1, NBins + 1):
                if ProgramROCHistogram.GetBinContent(i) < 5:
                    self.ResultData['HiddenData']['ROCsNotProgrammable'].append(i)
            NROCsNotProgrammable = len(self.ResultData['HiddenData']['ROCsNotProgrammable'])
            self.ResultData['KeyValueDictPairs']['NROCsNotProgrammable']['Value'] = NROCsNotProgrammable

        # draw plot if data exists
        if IanaLossPerRoc:

            LowIanaLossRocs = [x for x in IanaLossPerRoc if x < 15.0]

            if len(LowIanaLossRocs) > 1:
                self.ResultData['KeyValueDictPairs']['IanaLossProblems']['Value'] = 'Yes'
                self.ResultData['HiddenData']['IanaLossProblems'] = True
            elif len(LowIanaLossRocs) > 0:
                self.ResultData['KeyValueDictPairs']['IanaLossProblems']['Value'] = 'Only single ROC below'
            else:
                self.ResultData['KeyValueDictPairs']['IanaLossProblems']['Value'] = 'No'

            self.ResultData['KeyValueDictPairs']['Mean']['Value'] = '{0:1.2f}'.format(float(sum(IanaLossPerRoc)) / len(IanaLossPerRoc) if len(IanaLossPerRoc) > 0 else -1)
            self.ResultData['KeyValueDictPairs']['Min']['Value'] = '{0:1.2f}'.format(float(min(IanaLossPerRoc)) if len(IanaLossPerRoc) > 0 else -1)
            self.ResultData['KeyValueDictPairs']['Max']['Value'] = '{0:1.2f}'.format(float(max(IanaLossPerRoc)) if len(IanaLossPerRoc) > 0 else -1)

            for iRoc in range(0, NChips):
                self.ResultData['Plot']['ROOTObject'].SetBinContent(iRoc + 1, IanaLossPerRoc[iRoc])

            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetRangeUser(0, float(max(IanaLossPerRoc))*1.1 if len(IanaLossPerRoc) > 0 else 25)
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].Draw()

            IanaLossThr = self.TestResultEnvironmentObject.GradingParameters['IanaLossThr']
            self.ResultData['Plot']['ROOTObject_LowEdge'] = ROOT.TCutG('lLower', 2)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetPoint(0, 0, IanaLossThr)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetPoint(1, NChips, IanaLossThr)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetLineColor(ROOT.kRed)
            self.ResultData['Plot']['ROOTObject_LowEdge'].SetLineStyle(2)
            self.ResultData['Plot']['ROOTObject_LowEdge'].Draw('same')

            self.SaveCanvas()

        # hide box otherwise
        else:
            self.DisplayOptions['Show'] = False
            self.ResultData['Plot']['ROOTObject'] = None



