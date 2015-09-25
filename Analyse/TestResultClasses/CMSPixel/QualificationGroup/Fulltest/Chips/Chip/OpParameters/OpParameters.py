import ROOT
import glob
import AbstractClasses
import os
import re
from operator import itemgetter

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_OpParameters_TestResult'
        self.NameSingle = 'OpParameters'

        self.ResultData['HiddenData']['DacParameters'] = {}
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    def PopulateResultData(self):
        Directory = self.RawTestSessionDataPath

        vcalTrim = 0
        foundParametersFile = False
        trimVcalString = ''
        
        # try to get the value from the fulltest logfile
        if self.ParentObject.ParentObject.ParentObject.trimVcal:
            vcalTrim = self.ParentObject.ParentObject.ParentObject.trimVcal
            DacParametersFileName = '{Directory}/dacParameters{trimVcal}_C{ChipNo}.dat'.format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'],trimVcal=vcalTrim)
            if os.path.isfile(DacParametersFileName):
                foundParametersFile = True
                trimVcalString = str(vcalTrim)

        # otherwise pick the newest one
        if not foundParametersFile:
            # get all dacParameters files
            dacfilename = '{Directory}/dacParameters*_C{ChipNo}.dat'.format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'])
            names = glob.glob(dacfilename)
            # sort by creation date
            names.sort(key=lambda x: os.stat(os.path.join('', x)).st_mtime)
            names = [(os.stat(os.path.join('', x)).st_mtime, x) for x in names]
            names.sort(key = itemgetter(0))
            # get newest file
            name = names[-1][1]
            DacParametersFileName = name
            name = name.split('/')[-1]

            vcalTrim = map(int, re.findall(r'\d+', name))
            if len(vcalTrim )==2:
                vcalTrim=vcalTrim[0]
                trimVcalString = str(vcalTrim)
            else:
                vcalTrim =-1
                trimVcalString = ''

        if os.path.exists(DacParametersFileName):
            DacParametersFile = open(DacParametersFileName, "r")
            self.ResultData['HiddenData']['DacParameters']['File'+trimVcalString] = DacParametersFile

            if DacParametersFile :
                for line in DacParametersFile:
                    results  = line.strip().split()
                    if len(results) == 2:
                        Key, ParameterValue = results
                    else:
                        a, Key, ParameterValue = results

                    if Key.lower() in ['viref_adc','ibias_dac']:
                        Key = 'PHScale'
                    if Key.lower() in ['voffsetro','voffsetr0']:
                        Key = 'PHOffset'
                    Key = Key.lower()
                    self.ResultData['HiddenData']['DacParameters'][Key] = ParameterValue
                DacParametersFile.close()

        self.ResultData['HiddenData']['vcalTrim'] = vcalTrim
        self.ResultData['HiddenData']['DacParameters']['vcaltrim'] = trimVcalString
        ParameterList = [
            'vcalTrim',
            'Vana',
            'CalDel',
            'VthrComp',
            'Vtrim',
            'PHScale',
            'PHOffset',
        ]
        if self.ResultData['HiddenData']['DacParameters'].has_key('VoffsetOp'):
            ParameterList.append('VoffsetOp')

        for trimVcalString in ParameterList:
            if self.ResultData['HiddenData']['DacParameters'].has_key(trimVcalString.lower()):
                ParameterValue = self.ResultData['HiddenData']['DacParameters'][trimVcalString.lower()]
            else:
                ParameterValue = 'N/A'

            self.ResultData['KeyValueDictPairs'][trimVcalString] = {
                'Value':ParameterValue,
                #'Unit':'',
            }
            self.ResultData['KeyList'].append(trimVcalString)
