                                      # -*- coding: utf-8 -*-
import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
from AbstractClasses.GeneralTestResult import GeneralTestResult
import os

class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_DacParameterOverview_TestResult'
        self.NameSingle = 'DacParameterOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
        Directory = self.RawTestSessionDataPath
        for i in ['']+range(10,100,10):
        		DacParametersFileName = "{Directory}/DacParameters{DacParameterSetValue}_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'],DacParameterSetValue=str(i))
        		if os.path.isfile(DacParametersFileName):
        	        	        	DacParametersFile = open(DacParametersFileName, "r")
        	        	        	if DacParametersFile:
        	        	        		self.ResultData['SubTestResultDictList'] += [
        	        	        		{
        	        	        			'Key':'DacParameters'+str(i),
        	        	        			'Module': 'DacParameters',
        	        	        			'InitialAttributes': {
        	        	        				'DacParametersFile':DacParametersFile,
        	        	        				'DacParameterSetValue':str(i)
        	        	        			},
        	        	        		},
        	        	        	]

