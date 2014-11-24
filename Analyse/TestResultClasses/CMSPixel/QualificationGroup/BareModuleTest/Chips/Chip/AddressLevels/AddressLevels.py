import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.AddressLevels.AddressLevels
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.AddressLevels.AddressLevels.TestResult):
    def CustomInit(self):
    	# Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_AddressLevels_TestResult'
        self.NameSingle='AddressLevels'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
        

        
#    def PopulateResultData(self):

        #
        # Already implemented in Fulltest, then import from there the histogram
        #
        

