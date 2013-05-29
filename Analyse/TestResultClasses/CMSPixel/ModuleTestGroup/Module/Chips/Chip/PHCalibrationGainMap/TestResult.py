import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
	def CustomInit(self):
		self.Name='CMSPixel_ModuleTestGroup_Module_Chips_Chip_PHCalibrationGainMap_TestResult'
		self.NameSingle='PHCalibrationGainMap'
		self.Attributes['TestedObjectType'] = 'CMSPixel_ModuleTestGroup_Module_ROC'
		
	def SetStoragePath(self):
		pass
		
	def PopulateResultData(self):
		
		self.ResultData['Plot']['ROOTObject'] =  self.ParentObject.ResultData['SubTestResults']['PHCalibrationGain'].ResultData['Plot']['ROOTObject_hGainMap']
		ROOT.gPad.SetLogy(0)
		if (self.ResultData['Plot']['ROOTObject']):
			self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
			self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
			self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
			self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
			self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
			self.ResultData['Plot']['ROOTObject'].Draw("colz");
		if self.SavePlotFile:
			self.Canvas.SaveAs(self.GetPlotFileName())		
		self.ResultData['Plot']['Enabled'] = 1
		self.Title = 'PH Calibration Gain Map'
		self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
