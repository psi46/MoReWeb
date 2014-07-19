import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_TestResult'
        self.NameSingle='Chips'

        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        print 'nChips', self.ParentObject.Attributes['NumberOfChips'],type(self.ParentObject.Attributes['NumberOfChips'])
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
                    'StartChip': self.Attributes['StartChip']
                },
            })

    def append_target(self,SubTestResult_template):
        print 'appending target ',SubTestResult_template['Key']
        for i in self.ResultData['SubTestResultDictList']:
            if i['Key'].startwith('Chip'):
                print 'append to ',i['Key']

    def OpenFileHandle(self):
        self.FileHandle = self.ParentObject.FileHandle
    def PopulateResultData(self):
        pass
