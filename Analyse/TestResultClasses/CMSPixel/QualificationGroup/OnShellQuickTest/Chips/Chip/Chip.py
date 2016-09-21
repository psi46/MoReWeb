import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        ROOT.gStyle.SetOptStat(0)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_OnShellQuickTest_ROC'

        self.Name = 'CMSPixel_QualificationGroup_OnShellQuickTest_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+ str(self.Attributes['ChipNo'])

        self.ResultData['SubTestResultDictList'] = [
                {'Key':'PixelAlive',
                    'DisplayOptions':{
                        'Order': 100,
                    }
                },
                {'Key':'CalDelVthrcomp',
                    'DisplayOptions':{
                        'Order': 00,
                    }
                },
                {'Key':'BumpBonding',
                    'DisplayOptions':{
                        'Order': 120,
                    }
                },

            ]
#'PixelMap'

    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()

