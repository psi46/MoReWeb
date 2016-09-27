import AbstractClasses
import AbstractClasses.Helper.ROOTConfiguration as ROOTConfiguration
import os

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        ROOTConfiguration.initialise_ROOT()
        self.NameSingle = 'DACs'
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_{NameSingle}_TestResult'.format(NameSingle=self.NameSingle)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_OnShellQuickTest_ROC'
        self.chipNo = self.ParentObject.Attributes['ChipNo']

    def PopulateResultData(self):

        DACsFileName = self.RawTestSessionDataPath + '/dacParameters_C%d.dat'%self.chipNo
        if os.path.isfile(DACsFileName):
            DACLines = []
            try:
                with open(DACsFileName, 'r') as DACsFile:
                    DACLines = DACsFile.readlines()
            except:
                print "\x1b[31mERROR: could not read DACs file\x1b[0m"

            DACs = []
            for Line in DACLines:
                DACs.append([x for x in Line.strip().replace('\t',' ').split(' ') if len(x.strip()) > 0])

            for DAC in DACs:
                key = 'DAC_%s'%DAC[1].lower()
                self.ResultData['KeyValueDictPairs'][key] = {'Value': DAC[2], 'Label': '%s (%s)'%(DAC[1], DAC[0])}
                self.ResultData['KeyList'].append(key)
        else:
            self.ResultData['KeyValueDictPairs']['error'] = {'Value': 'dacParameters_C%d.dat not found'%self.chipNo, 'Label': 'DAC file'}
            self.ResultData['KeyList'].append('error')
