import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
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
                        'Order':12,
                    }
                }, # depends on PHCalibrationGain
                {'Key':'TrimBits',
                    'DisplayOptions':{
                        'Order':13,
                    }
                },
                {'Key':'TrimBitMap',
                    'DisplayOptions':{
                        'Order':14,
                    }
                },
                {'Key':'PHCalibrationGainMap',
                    'DisplayOptions':{
                        'Order':15,
                    }
                },  # depends on PHCalibrationGain

                {'Key':'OpParameters',
                    'DisplayOptions':{
                        'Order':16,
                    }
                },

                {'Key':'TrimBitProblems',
                    'DisplayOptions':{
                        'Order':17,
                    }
                },
                #{'Key':'TemperatureCalibration'},
                {'Key':'Summary',
                    'DisplayOptions':{
                        'Order':8,
                    }
                },


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
