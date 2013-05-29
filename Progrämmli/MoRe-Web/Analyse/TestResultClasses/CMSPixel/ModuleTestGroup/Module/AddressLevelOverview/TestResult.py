import AbstractClasses
import ROOT
import shutil
import os
import copy

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
	def CustomInit(self):
		self.Name='CMSPixel_ModuleTestGroup_Module_AddressLevelOverview_TestResult'
		self.NameSingle='AddressLevelOverview'
		self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
		
		for i in range(self.ParentObject.Attributes['NumberOfChips']-self.ParentObject.Attributes['StartChip']):
			self.ResultData['SubTestResultDictList'].append( {
				'Key':'Chip'+str(i), 
				'Module':'AddressLevels',
				'InitialAttributes':{
					'ChipNo':i,
					'StorageKey':'Chip'+str(i)
				},
			})
		
	def PopulateResultData(self):
		pass
			
	
