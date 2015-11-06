import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Chips_Chip_Grading_TestResult'
        self.NameSingle='Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = None

    def OpenFileHandle(self):
    	pass
  
    def PopulateResultData(self):
        pass
