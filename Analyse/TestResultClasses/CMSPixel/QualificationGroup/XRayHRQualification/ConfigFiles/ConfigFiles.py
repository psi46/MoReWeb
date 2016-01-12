# -*- coding: utf-8 -*-
import AbstractClasses
import glob
from AbstractClasses.Helper.BetterConfigParser import BetterConfigParser

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle = 'ConfigFiles'
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_%s_TestResult'%self.NameSingle
        self.Title = 'Test Environment'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

        self.ResultData['KeyValueDictPairs']['TestCenter'] = {'Label': 'Test Center', 'Value': ''}
        self.ResultData['KeyValueDictPairs']['Hostname'] = {'Label': 'Host name', 'Value': ''}


    def PopulateResultData(self):

        try:
            iniFileDict = BetterConfigParser()
            confFileDict = BetterConfigParser()

            iniFileSearchString = self.RawTestSessionDataPath + "/configfiles/*.ini"
            iniFiles = glob.glob(iniFileSearchString)
            if len(iniFiles) == 1:
                iniFileDict.read(iniFiles[0])

            confFileSearchString = self.RawTestSessionDataPath + "/configfiles/*.conf"
            confFiles = glob.glob(confFileSearchString)
            if len(confFiles) == 1:
                confFileDict.read(confFiles[0])

            try:
                self.ResultData['KeyValueDictPairs']['TestCenter']['Value'] = iniFileDict.get('OperationDetails', 'TestCenter')
            except:
                pass

            try:
                self.ResultData['KeyValueDictPairs']['Hostname']['Value'] =  iniFileDict.get('OperationDetails', 'Hostname')
            except:
                pass

        except:
            print "no .conf/.ini file found in 'configfiles' directory!"
            pass


