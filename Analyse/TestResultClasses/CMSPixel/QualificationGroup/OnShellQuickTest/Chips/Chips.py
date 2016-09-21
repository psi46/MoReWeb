import AbstractClasses
import ROOT


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_TestResult'
        self.NameSingle = 'Chips'

        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        for i in range(self.ParentObject.Attributes['NumberOfChips'] - self.ParentObject.Attributes['StartChip']):
            self.ResultData['SubTestResultDictList'].append({
                'Key': 'Chip' + str(i),
                'Module': 'Chip',
                'InitialAttributes': {
                    'ChipNo': i,
                    'StorageKey': 'Chip' + str(i),
                    'ModuleVersion': self.Attributes['ModuleVersion']
                },
            })

    def OpenFileHandle(self):
        self.FileHandle = self.ParentObject.FileHandle

    def PopulateResultData(self):
        pass
