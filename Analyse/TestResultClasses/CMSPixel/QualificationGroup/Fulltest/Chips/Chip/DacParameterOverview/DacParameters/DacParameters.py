# -*- coding: utf-8 -*-
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_DacParameterOverview_DacParameters_TrimBitParameters'+str(self.Attributes['DacParameterSetValue'])+'_TestResult'
        self.NameSingle='DacParameters'+str(self.Attributes['DacParameterSetValue'])
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

    def PopulateResultData(self):
        ChipNo=self.ParentObject.ParentObject.Attributes['ChipNo']
        DacParametersFile = self.Attributes['DacParametersFile']
        
        if not DacParametersFile:
            raise Exception('Cannot find DacParametersFile')
        else:
            for Line in DacParametersFile:
		LineArray = Line.strip().split()
		DacParameterName = LineArray[1]
		DacParameterValue = int(LineArray[2])
		self.ResultData['KeyValueDictPairs'][DacParameterName] = {
				'Value': '{0:1.0f}'.format(DacParameterValue),
				'Label': DacParameterName
		}
		self.ResultData['KeyList'] += [DacParameterName]
