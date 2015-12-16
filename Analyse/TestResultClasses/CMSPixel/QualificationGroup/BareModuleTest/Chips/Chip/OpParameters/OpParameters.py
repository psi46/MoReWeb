import ROOT
import AbstractClasses
import TestResultClasses
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.OpParameters.OpParameters

class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.OpParameters.OpParameters.TestResult):


    def CustomInit(self):
    	# Call Overridden CustomInit()
    	super(TestResult, self).CustomInit()
    	
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_OpParameters_TestResult'
        self.NameSingle = 'OpParameters'
        self.ResultData['HiddenData']['DacParameters'] = {}
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'



