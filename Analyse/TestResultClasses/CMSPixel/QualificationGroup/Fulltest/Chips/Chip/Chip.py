import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        ROOT.gStyle.SetOptStat(0)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])
        # order!
        self.ResultData['SubTestResultDictList'] = []

        if self.Attributes['ModuleVersion'] == 1:
            self.ResultData['SubTestResultDictList'] += [
                {
                    'Key':'PHCalibrationTan',
                    'DisplayOptions':{
                        'Show':False,
                    }
                }
            ]

        self.ResultData['SubTestResultDictList'] += [
                {'Key':'OpParameters',
                    'DisplayOptions':{
                        'Order':16,
                    }
                },
                {
                    'Key':'PixelMap',
                    'DisplayOptions':{
                        'Order':1,
                    }
                },
                {'Key':'SCurveWidths',
                    'DisplayOptions':{
                        'Order':2,
                    }
                },
                {'Key':'VcalThresholdUntrimmed',
                    'DisplayOptions':{
                        'Order':3,
                    }
                },# depends on SCurveWidths'''
                {'Key':'VcalThresholdTrimmed',
                    'DisplayOptions':{
                        'Order':4,
                    }
                },# depends on
                {'Key':'BumpBonding',
                    'DisplayOptions':{
                        'Order':6,
                    }
                },
                {'Key':'BumpBondingProblems',
                    'DisplayOptions':{
                        'Order':5,
                    }
                },
                {'Key':'BumpBondingMap',
                    'DisplayOptions':{
                        'Order':5,
                    }
                }
            ]

        self.ResultData['SubTestResultDictList'] += [
            {'Key':'BB4',
                'DisplayOptions':{
                    'Order':5,
                }
            }
        ]

        self.ResultData['SubTestResultDictList'] += [
                {'Key':'TrimBitTest',
                    'DisplayOptions':{
                        'Order':7,
                    }
                },
                {'Key':'AddressDecoding',
                    'DisplayOptions':{
                        'Order':9,
                    }
                },
                {'Key':'PHCalibrationGain',
                    'DisplayOptions':{
                        'Order':11,
                    }
                },

                {'Key':'PHCalibrationPedestal',
                    'DisplayOptions':{
                        'Order':13,
                    }
                }, # depends on PHCalibrationGain

                {'Key':'PHCalibrationParameter1',
                    'DisplayOptions':{
                        'Order':12,
                    }
                },
                {'Key':'TrimBits',
                    'DisplayOptions':{
                        'Order':14,
                    }
                },
                {'Key':'TrimBitMap',
                    'DisplayOptions':{
                        'Order':15,
                    }
                },
                {'Key':'PHCalibrationGainMap',
                    'DisplayOptions':{
                        'Order':16,
                    }
                },  # depends on PHCalibrationGain


                {'Key':'TrimBitProblems',
                    'DisplayOptions':{
                        'Order':17,
                    }
                },
                #{'Key':'TemperatureCalibration'},
                {'Key':'Grading',
                    'DisplayOptions':{
                        'Show':False,
                    }
                },
                {'Key':'Summary',
                    'DisplayOptions':{
                        'Order':8,
                    }
                },
                {'Key':'DacParameterOverview',
                    'DisplayOptions':{
                        
                    }#depends on TrimBits
                },
                {'Key':'PerformanceParameters',
                    'DisplayOptions':{
                    }
                },
                {'Key':'DacDac',
                    'DisplayOptions':{
                    }
                },
                {'Key':'ReadbackCal',
                    'DisplayOptions':{
                        
                    }
                }

            ]

        if not self.ParentObject.ParentObject.Attributes['isDigital']:
                self.ResultData['SubTestResultDictList'].append(
                                                            {'Key':'AddressLevels',
                                                                'DisplayOptions':{
                                                                    'Order':10,
                                                                }
                                                            }
                                                            )


    def PopulateResultData(self):
        self.CloseSubTestResultFileHandles()
