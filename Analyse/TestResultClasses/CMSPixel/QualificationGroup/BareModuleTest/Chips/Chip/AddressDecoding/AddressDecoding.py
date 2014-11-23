import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.AddressDecoding.AddressDecoding
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.AddressDecoding.AddressDecoding.TestResult):
    def CustomInit(self):
    	# Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
	self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_AddressDecoding_TestResult'
        self.NameSingle='AddressDecoding'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
        
