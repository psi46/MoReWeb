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
                {'Key':'AddressDecoding',
                    'DisplayOptions':{
                        'Order':2,
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
                {'Key':'DacDac',
                    'DisplayOptions':{
                    }
                },
                {'Key':'BB2Scan',
                    'DisplayOptions':{
                        'Order':31,
                    }
                },
                {'Key':'BareBBWidth',
                 'DisplayOptions':{
                    'Order':32,
                    }
                 },
                {'Key':'BB2Map',
                 'DisplayOptions':{
                    'Order':33,
                    }
                 },
                {'Key':'BB4',
                 'DisplayOptions':{
                    'Order':34,
                    }
                 },
                {'Key':'ReadbackCalIana',
                 'Module':'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCalIana',
                 'StorageKey':'ReadbackCalIana',
                    'DisplayOptions':{
                        'Show': True,
                        'Order': 50,
                    }
                },
                {'Key':'ReadbackCalVdig',
                 'Module':'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCalVdig',
                 'StorageKey':'ReadbackCalVdig',
                    'DisplayOptions':{
                        'Show': True,
                        'Order': 52,
                    }
                },
                {'Key':'ReadbackCalVana',
                 'Module':'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCalVana',
                 'StorageKey':'ReadbackCalVana',
                    'DisplayOptions':{
                        'Show': True,
                        'Order': 54,
                    }
                },
                {'Key':'ReadbackCal',
                 'Module':'TestResultClasses.CMSPixel.QualificationGroup.Fulltest.Chips.Chip.ReadbackCal',
                 'StorageKey':'ReadbackCal',
                    'DisplayOptions':{
                        'Show': True,
                        'Order': 60,
                    }
                },
                {'Key':'Grading',
                    'DisplayOptions':{
                        'Show': False
                    }
                },

            ]
#'PixelMap'

    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()

