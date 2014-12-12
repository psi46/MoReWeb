import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap.PixelMap
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.PixelMap.PixelMap.TestResult):
    def CustomInit(self):
    	# Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
        #ROOTConfiguration.initialise_ROOT()
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_PixelMapNew_TestResult'
        self.NameSingle='PixelMap'

    # PopulateResultData is inherited
