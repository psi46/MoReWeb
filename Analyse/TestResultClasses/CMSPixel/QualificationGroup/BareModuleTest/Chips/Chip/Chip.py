import AbstractClasses
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):


    def CustomInit(self):
        ROOT.gStyle.SetOptStat(0)
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'

        self.Name = 'CMSPixel_QualificationGroup_BareModuleTest_Chips_Chip_TestResult'
        self.NameSingle = 'Chip'
        self.Title = 'Chip '+str(self.Attributes['ChipNo'])
        # order!
        self.ResultData['SubTestResultDictList'] = []

        if self.Attributes['ModuleVersion'] == 1:
            self.ResultData['SubTestResultDictList'] += [
            ]

        print 'Chip TestSoftware: ', self.ParentObject.ParentObject.testSoftware

        if self.ParentObject.ParentObject.testSoftware == 'pxar':

            self.ResultData['SubTestResultDictList'] += [
                
                {'Key':'OpParameters',
                 'DisplayOptions':{
                        'Order':16,
                        }
                 },
#                {
#                    'Key':'BarePixelMap',
#                    'DisplayOptions':{
#                        'Order':2,
#                        }
#                    },
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
                {'Key':'AddressDecoding',
                    'DisplayOptions':{
                        'Order':9,
                    }
                },
                {'Key':'BareBBMap',
                    'DisplayOptions':{
                        'Order':1,
                    }
                },
                {'Key':'BareBBScan',
                    'DisplayOptions':{
                        'Order':1,
                    }
                },
                {'Key':'BareBBWidth',
                    'DisplayOptions':{
                        'Order':1,
                    }
                },
#                {'Key':'PixelMapNew',
#                    'DisplayOptions':{
#                        'Order':1,
#                    }
#                },
                 {'Key':'PixelMap',
                    'DisplayOptions':{
                        'Order':1,
                    }
                },                
                ]
            
            
        else:

            self.ResultData['SubTestResultDictList'] += [

                {'Key':'OpParameters',
                 'DisplayOptions':{
                        'Order':16,
                        }
                 },
                {
                    'Key':'BarePixelMap',
                    'DisplayOptions':{
                        'Order':2,
                        }
                    },
                {'Key':'BareBBMap',
                 'DisplayOptions':{
                        'Order':1,
                        }
                 },
                {'Key':'BareBBScan',
                 'DisplayOptions':{
                        'Order':1,
                        }
                 },
                {'Key':'BareBBWidth',
                 'DisplayOptions':{
                        'Order':1,
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
