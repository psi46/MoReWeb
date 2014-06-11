import ROOT
import glob
import AbstractClasses
import os
import re

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    
    
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_OpParameters_TestResult'
        self.NameSingle = 'OpParameters'
        
        self.ResultData['HiddenData']['DacParameters'] = {}
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        

        
    def PopulateResultData(self):
        Directory = self.RawTestSessionDataPath
        vcalTrim = 0
        dacfilename = '{Directory}/dacParameters*_C{ChipNo}.dat'.format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo']) 
        names = glob.glob(dacfilename)
        names.sort(key=lambda x: os.stat(os.path.join('', x)).st_mtime)
        name = names[-1]
        DacParametersFileName = name
        name = name.split('/')[-1]
        vcalTrim = map(int, re.findall(r'\d+', name))
        if len(vcalTrim )==2:
            vcalTrim=vcalTrim[0]
            i = str(vcalTrim) 
        else: 
            vcalTrim =-1
            i = ''

    
        if os.path.exists(DacParametersFileName):
#            if not vcalTrim:
#                try:
#                    vcalTrim = int(i)
#                except:
#                    vcalTrim  = -1
            DacParametersFile = open(DacParametersFileName, "r");
            self.ResultData['HiddenData']['DacParameters']['File'+i] = DacParametersFile
                
            if DacParametersFile :
                for line in DacParametersFile:
                    a, Key, ParameterValue = line.strip().split()
                    if Key.lower() in ['viref_adc','ibias_dac']:
                        Key = 'PHScale'
                    if Key.lower() in ['voffsetro','voffsetr0']:
                        Key = 'PHOffset'
                    self.ResultData['HiddenData']['DacParameters'][Key] = ParameterValue
                DacParametersFile.close()
        
        self.ResultData['HiddenData']['vcalTrim'] = vcalTrim
        self.ResultData['HiddenData']['DacParameters']['vcalTrim'] = vcalTrim
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

        for i in ParameterList:
            
            if self.ResultData['HiddenData']['DacParameters'].has_key(i):
                ParameterValue = self.ResultData['HiddenData']['DacParameters'][i]
            else:
                ParameterValue = 'N/A'
                
            self.ResultData['KeyValueDictPairs'][i] = {
                'Value':ParameterValue,
                #'Unit':'',
            }
            self.ResultData['KeyList'].append(i)
