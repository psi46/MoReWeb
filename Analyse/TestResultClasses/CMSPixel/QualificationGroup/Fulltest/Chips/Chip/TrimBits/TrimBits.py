# -*- coding: utf-8 -*-
import os
import glob
import ROOT

import AbstractClasses.Helper.HistoGetter as HistoGetter
import AbstractClasses


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TrimBits_TestResult'
        self.NameSingle = 'TrimBits'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        Directory = self.RawTestSessionDataPath
        FileNamePattern = '/[T,t]rim[p,P]arameters*_C{ChipNo}.dat'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        files = glob.glob('{Directory}/{FileNamePattern}'.format(Directory=Directory, FileNamePattern=FileNamePattern))
        for file in files:
            # print file
            f = file.split('/')[-1].split('.')[0].lower()
            # print f
            f = f.replace('trimparameters', '')
            # print f
            f = f.split('_')
            # print f
            if os.path.isfile(file):
                TrimParametersFile = open(file, "r")
                self.ResultData['SubTestResultDictList'] += [
                    {
                    'Key': 'TrimBitParameters' + str(f[0]),
                    'Module': 'TrimBitParameters',
                    'InitialAttributes': {
                    'TrimParametersFile': TrimParametersFile,
                    'TrimValue': str(f[0])
                    },
                    },
                ]


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)

        ChipNo = self.ParentObject.Attributes['ChipNo']
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict

        # load trimbit distribution from .root file or create from trim bit map
        if HistoDict.has_option(self.NameSingle, 'TrimBits'):
            histname = HistoDict.get(self.NameSingle, 'TrimBits')
            root_object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
        else:
            histname = HistoDict.get(self.NameSingle, 'TrimBitMap')
            root_object2 = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
            root_object = ROOT.TH1F(self.GetUniqueID(), 'TrimBitDistribution', 17, -.5, 16.5)
            for col in range(self.nCols):  # Columns
                for row in range(self.nRows):  # Rows
                    entry = root_object2.GetBinContent(col + 1, row + 1)
                    root_object.Fill(entry)

        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1F(self.GetUniqueID(), 'TrimBitDistribution', 17, -.5, 16.5)
        for bin in range(0, root_object.GetNbinsX() + 1):
            bin_content = root_object.GetBinContent(bin)
            bin_center = int(root_object.GetXaxis().GetBinCenter(bin))
            self.ResultData['Plot']['ROOTObject'].Fill(bin_center, bin_content)
        mean = 0
        rms = 0

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].SetFillStyle(3002)
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlack)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Trim bits")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, 15)

            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("entries")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('hist')

            mean = self.ResultData['Plot']['ROOTObject'].GetMean()
            rms = self.ResultData['Plot']['ROOTObject'].GetRMS()

        self.ResultData['KeyValueDictPairs'] = {
            'mu': {
                'Value': '{0:1.2f}'.format(mean),
                'Label': 'μ'
            },
            'sigma': {
                'Value': '{0:1.2f}'.format(rms),
                'Label': 'RMS'
            }
        }
        self.ResultData['KeyList'] = ['mu', 'sigma']

        self.Title = 'Trim Bits'
        self.SaveCanvas()
