import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        ROOT.gStyle.SetOptStat(0)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Reception_ROC'

        self.Name = 'CMSPixel_QualificationGroup_Reception_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])

        self.ResultData['SubTestResultDictList'] = [
                {'Key':'PixelMap',
                    'DisplayOptions':{
                        'Order':1,
                    }
                },
                {'Key':'BumpBonding',
                    'DisplayOptions':{
                        'Order':10,
                    }
                },
                {'Key':'BumpBondingProblems',
                    'DisplayOptions':{
                        'Order':20,
                    }
                },
                {'Key':'BumpBondingMap',
                    'DisplayOptions':{
                        'Order':30,
                    }
                },
                {'Key':'ReadbackCal',
                    'DisplayOptions':{
                        
                    }
                },
                {'Key':'Grading',
                    'DisplayOptions':{
                        'Show': False
                    }
                },
                {'Key':'DacDac',
                    'DisplayOptions':{
                    }
                }
            ]

    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()



       