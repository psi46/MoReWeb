# -*- coding: utf-8 -*-
import os
import glob

from AbstractClasses.GeneralTestResult import GeneralTestResult


class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_DacParameterOverview_TestResult'
        self.NameSingle = 'DacParameterOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        self.AddDacParameterSets()

    def AddDacParameterSets(self):
        Directory = self.RawTestSessionDataPath
        FileNamePattern = '/[d,D]ac[p,P]arameters*_C{ChipNo}.dat'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
        files = glob.glob('{Directory}/{FileNamePattern}'.format(Directory=Directory, FileNamePattern=FileNamePattern))
        for file in files:
            # print file
            f = file.split('/')[-1].split('.')[0].lower()
            # print f
            f = f.replace('dacparameters', '')
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