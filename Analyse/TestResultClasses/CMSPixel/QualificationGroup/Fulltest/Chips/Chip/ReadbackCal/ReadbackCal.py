import ROOT
import glob
import AbstractClasses
import os
import re
from operator import itemgetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_ReadbackCal_TestResult'
        self.NameSingle = 'ReadbackCal'

        self.ResultData['HiddenData']['ReadbackCal'] = {}
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


#            self.ResultData['KeyValueDictPairs']['TrimValue'] = {
#                'Value': '{0:}'.format(trim),
#                'Label': 'TrimValue'
#            }
#            self.ResultData['KeyList'] += ['TrimValue']
#        for Line in ReadbackFile:
#                LineArray = Line.strip().split()
#                RbCalParameterName = LineArray[0]
#
#                RbCalParameterValue = float(LineArray[1])
#                self.ResultData['KeyValueDictPairs'][RbCalParameterName.lower()] = {
#                    'Value': '{0:.2e}'.format(RbCalParameterValue),
#                    'Label': RbCalParameterName
#                }
#                self.ResultData['KeyList'] += [RbCalParameterName.lower()]
#            key = 'TrimBitParameters' + self.Attributes['DacParameterTrimValue']
#            object = \
#                self.ParentObject.ParentObject.ResultData['SubTestResults']['TrimBits'].ResultData['SubTestResults'][
#                    key]
#            self.ResultData['KeyValueDictPairs']['TrimBits_mu'] = object.ResultData['KeyValueDictPairs']['mu']
#            self.ResultData['KeyValueDictPairs']['TrimBits_mu']['Label'] = 'TrimBit Mean'
#            self.ResultData['KeyValueDictPairs']['TrimBits_sigma'] = object.ResultData['KeyValueDictPairs']['sigma']
#            self.ResultData['KeyValueDictPairs']['TrimBits_sigma']['Label'] = 'TrimBit sigma'
#            self.ResultData['KeyList'] += ['TrimBits_mu', 'TrimBits_sigma']


    def PopulateResultData(self):
        Directory = self.RawTestSessionDataPath
        # get all dacParameters files
#        FileNamePattern = '/readbackCal*_C{ChipNo}.dat'.format(ChipNo=self.ParentObject.Attributes['ChipNo'])
#        files = glob.glob('{Directory}/{FileNamePattern}'.format(Directory=Directory, FileNamePattern=FileNamePattern))
#        for file in files:
            
        rbfilename = '{Directory}/readbackCal*_C{ChipNo}.dat'.format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
        names = glob.glob(rbfilename)
        # sort by creation date
        names.sort(key=lambda x: os.stat(os.path.join('', x)).st_mtime)
        names = [(os.stat(os.path.join('', x)).st_mtime, x) for x in names]
        names.sort(key = itemgetter(0))
        # get newest file
        name = names[-1][1]
        ReadbackCalFileName = name
#        name = name.split('/')[-1]
#
#        vcalTrim = map(int, re.findall(r'\d+', name))
#        if len(vcalTrim )==2:
#            vcalTrim=vcalTrim[0]
#            i = str(vcalTrim)
#        else:
#            vcalTrim =-1
#            i = ''

        if os.path.exists(ReadbackCalFileName):
            ReadbackCalFile = open(ReadbackCalFileName, "r")
           # self.ResultData['HiddenData']['ReadbcakCal']['File'+i] = ReadbackCalFile

            if ReadbackCalFile :
                for Line in ReadbackCalFile:
                    LineArray = Line.strip().split()
                    RbCalParameterName = LineArray[0]

                    RbCalParameterValue = float(LineArray[1])
                    self.ResultData['KeyValueDictPairs'][RbCalParameterName.lower()] = {
                        'Value': '{0:.2e}'.format(RbCalParameterValue),
                        'Label': RbCalParameterName
                        }
                    self.ResultData['KeyList'] += [RbCalParameterName.lower()]
# results  = line.strip().split()
# if len(results) == 2:
#     Key, ParameterValue = results
# else:
#     a, Key, ParameterValue = results
#
# if Key.lower() in ['viref_adc','ibias_dac']:
#     Key = 'PHScale'
# if Key.lower() in ['voffsetro','voffsetr0']:
#     Key = 'PHOffset'
# Key = Key.lower()
# self.ResultData['HiddenData']['DacParameters'][Key] = ParameterValue
                ReadbackCalFile.close()
