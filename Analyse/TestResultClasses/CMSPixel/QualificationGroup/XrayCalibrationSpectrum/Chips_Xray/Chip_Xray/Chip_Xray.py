import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_TestResult'
        self.NameSingle='Chips'
        
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        print 'nChips', self.ParentObject.Attributes['NumberOfChips'],type(self.ParentObject.Attributes['NumberOfChips'])
        print 'startChip', self.ParentObject.Attributes['StartChip'],type(self.ParentObject.Attributes['StartChip'])

    def OpenFileHandle(self):
        self.FileHandle = self.ParentObject.FileHandle  
    def PopulateResultData(self):
        pass
