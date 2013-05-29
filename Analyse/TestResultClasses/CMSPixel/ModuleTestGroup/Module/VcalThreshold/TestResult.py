import ROOT
import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
	def CustomInit(self):
		self.Name='CMSPixel_ModuleTestGroup_Module_VcalThreshold_TestResult'
		self.NameSingle='VcalThreshold'
		self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
		self.Title = 'Vcal Threshold'
	def SetStoragePath(self):
		pass
		
	def PopulateResultData(self):
		
		
		ROOT.gStyle.SetOptStat(0);
		self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", 416, 0., 416., 160, 0., 160.); # mThreshold
		
		for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
			ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
			for j in range(52): # Columns
				for k in range(80): # Rows
					if ChipTestResultObject.Attributes['ChipNo'] < 8:
						tmpCol = 8*52-(ChipTestResultObject.Attributes['ChipNo']*52+j)
						tmpRow = 2*80-k
					else:
						tmpCol = (ChipTestResultObject.Attributes['ChipNo']%8*52+j)+1
						tmpRow = k+1
					if ChipTestResultObject.Attributes['ChipNo'] < 8:
						tmpRow += 80
					# Get the data from the chip sub test result VcalThresholdUntrimmed
					self.ResultData['Plot']['ROOTObject'].SetBinContent(tmpCol, tmpRow, ChipTestResultObject.ResultData['SubTestResults']['VcalThresholdUntrimmed'].ResultData['Plot']['ROOTObject'].GetBinContent(j+1, k+1))
		
		
		
		if self.ResultData['Plot']['ROOTObject']:
			mThresholdMin = 0.
			mThresholdMax = 255.

			if  self.ResultData['Plot']['ROOTObject'].GetMaximum() < mThresholdMax: 
				mThresholdMax = self.ResultData['Plot']['ROOTObject'].GetMaximum();
			
			if self.ResultData['Plot']['ROOTObject'].GetMinimum() > mThresholdMin:
				mThresholdMin = self.ResultData['Plot']['ROOTObject'].GetMinimum();
			
			
			self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(mThresholdMin,mThresholdMax);
			self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
			self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
			self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle();
			self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5);
			self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle();
			self.ResultData['Plot']['ROOTObject'].Draw('colz');
		
		
		box = ROOT.TBox();
		box.SetFillColor(3);
		box.SetFillStyle(3004);
		if self.ParentObject.Attributes['NumberOfChips'] < 16 and self.ParentObject.Attributes['StartChip'] == 0: 
			box.SetFillColor(29);
			box.DrawBox( 0, 0,  416,  80);
		elif self.ParentObject.Attributes['NumberOfChips'] < 16 and self.ParentObject.Attributes['StartChip'] == 8:
			box.SetFillColor(29);
			box.DrawBox( 0, 0,  416,  160);
		
		self.ResultData['Plot']['Format'] = 'png'
		
		if self.SavePlotFile:
			self.Canvas.SaveAs(self.GetPlotFileName())		
		self.ResultData['Plot']['Enabled'] = 1
		self.ResultData['Plot']['Caption'] = 'Vcal Threshold'
		self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
