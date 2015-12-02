import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        ROOT.gStyle.SetOptStat(0)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_SingleTest_ROC'

        self.Name = 'CMSPixel_QualificationGroup_SingleTest_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])

        for ChipTest in self.Attributes['Tests']:
            self.ResultData['SubTestResultDictList'].append(
                {
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
                })


    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
