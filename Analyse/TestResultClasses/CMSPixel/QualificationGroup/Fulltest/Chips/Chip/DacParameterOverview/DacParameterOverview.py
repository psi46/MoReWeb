# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
from AbstractClasses.GeneralTestResult import GeneralTestResult
import os
import glob


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_DacParameterOverview_TestResult'
        self.NameSingle = 'DacParameterOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        Directory = self.RawTestSessionDataPath
        for i in [''] + range(10, 100, 10):
            DacParametersFileName = "{Directory}/DacParameters{DacParameterSetValue}_C{ChipNo}.dat".format(
                Directory=Directory, ChipNo=self.ParentObject.Attributes['ChipNo'], DacParameterSetValue=str(i))
            if os.path.isfile(DacParametersFileName):
                DacParametersFile = open(DacParametersFileName, "r")
                if DacParametersFile:
                    self.ResultData['SubTestResultDictList'] += [
                        {
                        'Key': 'DacParameters' + str(i),
                        'Module': 'DacParameters',
                        'InitialAttributes': {
                        'DacParametersFile': DacParametersFile,
                        'DacParameterTrimValue': str(i)
                        },
                        },
                    ]

    def AddDacParameterSets(self):
        Directory = self.RawTestSessionDataPath
        FileNamePattern = '/[d,D]ac[p,P]arameters*_C{ChipNo}.dat'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
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
                DacParametersFile = open(file, "r")
                self.ResultData['SubTestResultDictList'] += [
                    {
                    'Key': 'DacParameters' + str(f[0]),
                    'Module': 'DacParameters',
                    'InitialAttributes': {
                        'DacParametersFile': DacParametersFile,
                        'DacParameterTrimValue': str(f[0])
                        },
                    },
                ]