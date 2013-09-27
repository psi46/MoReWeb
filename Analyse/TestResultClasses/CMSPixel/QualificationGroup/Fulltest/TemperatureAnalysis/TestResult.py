# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_TemperatureAnalysis_TestResult'
        self.NameSingle='TemperatureAnalysis'
#        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Temperature Analysis'
        
    def SetStoragePath(self):
        pass
        
    def PopulateResultData(self):
        Directory = self.ParentObject.RawTestSessionDataPath
        temperatureFile =  "{Directory}/temperature.log".format(Directory=Directory);
        meanTemp = 0
        sigmaTemp = 0
        self.ResultData['KeyValueDictPairs']['MeanTemperature'] = {'Value': meanTemp, 'Sigma': sigmaTemp, 'Unit': "degC"}
#        self.ResultData['KeyValueDictPairs']['SigmaTemperature'] = {'Value': sigmaTemp, 'Unit': "degC"}
        self.ResultData['KeyList'].append('MeanTemperature')
        
