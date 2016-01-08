# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
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
            }
        }
        self.ResultData['KeyList'] = ['IanaLossProblems', 'Mean', 'Min', 'Max']

    def PopulateResultData(self):

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

        # draw plot if data exists
        if IanaLossPerRoc:

            if IanaLossProblems:
                self.ResultData['KeyValueDictPairs']['IanaLossProblems']['Value'] = 'Yes'
            else:
                self.ResultData['KeyValueDictPairs']['IanaLossProblems']['Value'] = 'No'

            self.ResultData['KeyValueDictPairs']['Mean']['Value'] = '{0:1.2f}'.format(float(sum(IanaLossPerRoc)) / len(IanaLossPerRoc) if len(IanaLossPerRoc) > 0 else -1)
            self.ResultData['KeyValueDictPairs']['Min']['Value'] = '{0:1.2f}'.format(float(min(IanaLossPerRoc)) if len(IanaLossPerRoc) > 0 else -1)
            self.ResultData['KeyValueDictPairs']['Max']['Value'] = '{0:1.2f}'.format(float(max(IanaLossPerRoc)) if len(IanaLossPerRoc) > 0 else -1)

            for iRoc in range(0, NChips):
                self.ResultData['Plot']['ROOTObject'].SetBinContent(iRoc + 1, IanaLossPerRoc[iRoc])
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



