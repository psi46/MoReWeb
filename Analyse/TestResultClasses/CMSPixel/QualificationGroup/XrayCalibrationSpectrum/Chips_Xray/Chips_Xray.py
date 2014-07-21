import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Xray_Chips_TestResult'
        self.NameSingle='Chips_Xray'
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag

        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        if self.verbose:
            print 'nChips', self.ParentObject.Attributes['NumberOfChips'],type(self.ParentObject.Attributes['NumberOfChips'])
        if self.verbose:
            print 'startChip', self.ParentObject.Attributes['StartChip'],type(self.ParentObject.Attributes['StartChip'])
        for i in range(self.ParentObject.Attributes['NumberOfChips']-self.ParentObject.Attributes['StartChip']):
            self.ResultData['SubTestResultDictList'].append( {
                'Key':'Chip_Xray'+str(i),
                'Module':'Chip_Xray',
                'InitialAttributes':{
                    'ChipNo':i,
                    'StorageKey':'Chip_Xray'+str(i),
                    'ModuleVersion':self.Attributes['ModuleVersion'],
                    'NumberOfChips': self.Attributes['NumberOfChips'],
                    'StartChip': self.Attributes['StartChip'],
                    'SubTestResultDictList':self.Attributes["SubTestResultDictList"]
                },
            })

    def OpenFileHandle(self):
        self.FileHandle = self.ParentObject.FileHandle

    def PopulateResultData(self):
        pass
