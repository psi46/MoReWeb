import ROOT
import AbstractClasses
import ROOT
import os
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    
    
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_OpParameters_TestResult'
        self.NameSingle = 'OpParameters'
        
        self.ResultData['HiddenData']['DacParameters'] = {}
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        Directory = self.FullTestResultsPath
        vcalTrim = 0
        for i in ['60', '50', '']:
            DacParametersFileName =  "{Directory}/dacParameters{i}_C{ChipNo}.dat".format(Directory=Directory,i=i, ChipNo=self.ParentObject.Attributes['ChipNo']);
            if os.path.exists(DacParametersFileName):
                if not vcalTrim:
                    vcalTrim = int(i)
                
                DacParametersFile = open(DacParametersFileName, "r");
                self.ResultData['HiddenData']['DacParameters']['File'+i] = DacParametersFile
                    
                if DacParametersFile :
                    for line in DacParametersFile:
                        a, Key, ParameterValue = line.strip().split()
                        self.ResultData['HiddenData']['DacParameters'][Key] = ParameterValue
                    DacParametersFile.close()
        
        self.ResultData['HiddenData']['vcalTrim'] = vcalTrim
        ParameterList = [
            'Vana',
            'CalDel',
            'VthrComp',
            'Vtrim',
            'Ibias_DAC',
            'VoffsetOp'
        ]
        for i in ParameterList:
            
            if self.ResultData['HiddenData']['DacParameters'].has_key(i):
                ParameterValue = self.ResultData['HiddenData']['DacParameters'][i]
            else:
                ParameterValue = 'N/A'
                
            self.ResultData['KeyValueDictPairs'][i] = {
                'Value':ParameterValue,
                'Unit':'DAC',
            }
            self.ResultData['KeyList'].append(i)
