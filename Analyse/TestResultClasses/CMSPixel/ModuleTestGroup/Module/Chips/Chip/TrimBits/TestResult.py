import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
	def CustomInit(self):
		self.Name='CMSPixel_ModuleTestGroup_Module_Chips_Chip_TrimBits_TestResult'
		self.NameSingle='TrimBits'
		self.Attributes['TestedObjectType'] = 'CMSPixel_ModuleTestGroup_Module_ROC'
		
	def SetStoragePath(self):
		pass
		
	def PopulateResultData(self):
		

		
		ROOT.gStyle.SetOptStat(0);
		self.ResultData['Plot']['ROOTObject'] =  ROOT.TH2D(self.GetUniqueID(), "", 52, 0., 52., 80, 0., 80., ) # htm
		# TH2D
		self.ResultData['Plot']['ROOTObject_TrimMap'] =   self.ParentObject.ParentObject.FileHandle.Get("TrimMap_C{ChipNo};8".format(ChipNo=self.ParentObject.Attributes['ChipNo']) ).Clone(self.GetUniqueID())
		
		
		if self.ResultData['Plot']['ROOTObject']:
			for i in range(52): # Columns
				for j in range(80): # Rows
					self.ResultData['Plot']['ROOTObject'].SetBinContent(i+1, j+1, self.ResultData['Plot']['ROOTObject_TrimMap'].GetBinContent(i+1, j+1))
			
			self.ResultData['Plot']['ROOTObject'].SetTitle("");
			self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0., 16.);
			self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
			self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
			self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
			self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
			self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
			self.ResultData['Plot']['ROOTObject'].Draw('colz');
			

		if self.SavePlotFile:
			self.Canvas.SaveAs(self.GetPlotFileName())		
		self.ResultData['Plot']['Enabled'] = 1
		self.Title = 'Trim Bits'
		self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
