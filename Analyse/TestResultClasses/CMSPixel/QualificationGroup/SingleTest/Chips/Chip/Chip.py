import AbstractClasses
import copy

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_SingleTest_ROC'

        self.Name = 'CMSPixel_QualificationGroup_SingleTest_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])

        for ChipTest in self.Attributes['Tests']:

            if type(ChipTest) is dict:
                SubtestDict = copy.deepcopy(ChipTest)
                if not 'InitialAttributes' in SubtestDict:
                    SubtestDict['InitialAttributes'] = {}

                if 'StorageKey' in SubtestDict['InitialAttributes']:
                    StorageKey = SubtestDict['InitialAttributes']['StorageKey']
                elif 'Key' in SubtestDict:
                    StorageKey = SubtestDict['Key']
                elif 'Module' in SubtestDict:
                    StorageKey = SubtestDict['Module']
                else:
                    StorageKey = 'Subtest'

                SubtestDict['InitialAttributes'].update({
                            'ChipNo': self.Attributes['ChipNo'],
                            'StorageKey':'Chip%d_%s'%(self.Attributes['ChipNo'], StorageKey),
                            'ModuleVersion':self.Attributes['ModuleVersion'],
                })

                print "ST KEY:", 'Chip%d_%s'%(self.Attributes['ChipNo'], StorageKey)
            else:
                SubtestDict = {
                        'Key': ChipTest.split('.')[-1],
                        'Module': ChipTest,
                        'DisplayOptions': {
                            'Order': 100,
                            'Show': True,
                        },
                        'InitialAttributes':{
                            'ChipNo': self.Attributes['ChipNo'],
                            'StorageKey':'Chip%d_%s'%(self.Attributes['ChipNo'], ChipTest.split('.')[-1]),
                            'ModuleVersion':self.Attributes['ModuleVersion'],
                        },
                    }

            self.ResultData['SubTestResultDictList'].append(SubtestDict)


    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
