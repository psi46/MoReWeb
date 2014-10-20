import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import CMSPixel.QualificationGroup.Fulltest.Chips.Chip.AddressLevels.PopulateResultData as PopulateResultData
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_AddressLevels_TestResult'
        self.NameSingle='AddressLevels'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_BareModuleTest_ROC'
        

        
#    def PopulateResultData(self):

        #
        # Already implemented in Fulltest, then import from there the histogram
        #
        

