import ROOT
import AbstractClasses
import ROOT
import TestResultClasses.CMSPixel.QualificationGroup.Fulltest.BumpBondingMap.BumpBondingMap
class TestResult(TestResultClasses.CMSPixel.QualificationGroup.Fulltest.BumpBondingMap.BumpBondingMap.TestResult):
    def CustomInit(self):
        # Call Overridden CustomInit()
        super(TestResult, self).CustomInit()
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle='BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.ResultData['HiddenData']['SpecialBumpBondingTestName'] = ''

    # PopulateResultData is inherited
    
