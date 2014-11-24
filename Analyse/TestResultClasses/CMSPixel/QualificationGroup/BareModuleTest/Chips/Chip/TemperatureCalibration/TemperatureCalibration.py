import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.TemperatureCalibration.TemperatureCalibration
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.TemperatureCalibration.TemperatureCalibration.TestResult):


    def CustomInit(self):
        # Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
	self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TemperatureCalibration_TestResult'
        self.NameSingle = 'TemperatureCalibration'
        self.Enabled = False
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'
