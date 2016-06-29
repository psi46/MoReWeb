import ROOT
import AbstractClasses
import os, json

from AbstractClasses.Helper.SetEncoder import SetEncoder

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self, TestResultEnvironmentObject = 0):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject

        self.singleSubtest = self.Attributes['SingleSubtest']

        if self.singleSubtest:
            self.HTMLFileName = 'ProductionOverview_%s.html'%('_'.join(self.singleSubtest))
        else:
            self.HTMLFileName = 'ProductionOverview.html'

        self.ImportPath = 'OverviewClasses.CMSPixel.ProductionOverview.ProductionOverviewPage'

        self.NameSingle = 'ProductionOverviewPage'
        self.Name = 'CMSPixel_ProductionOverview_%s'%self.NameSingle

        self.SaveHTML = True

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        NumModules = len(ModuleIDsList)
        NumModulesMaxPerList = 50

        self.SumJSONFilesModules = []

        SingleMinus20TestName = "m20_2"
        try:
            RequiredQualificationTypes = self.TestResultEnvironmentObject.Configuration['RequiredTestTypesForComplete'].strip().split(',')
            if "m20_2" not in RequiredQualificationTypes:
                print "No -20C test after cycling (m20_2) found!"
                if "m20_1" in RequiredQualificationTypes:
                    SingleMinus20TestName = "m20_1"
                    print "=> using m20_1 instead!"
                elif "p17_1" in RequiredQualificationTypes:
                    SingleMinus20TestName = "p17_1"
                    print "=> using p17_1 instead!"
                else:
                    print "\x1b[31mno equivalent test found!\x1b[0m"
        except:
            print "\x1b[31Could not decide which m20 test to use, check 'RequiredTestTypesForComplete' field in configuration!\x1b[0m"

        TestsList = ['m20_1', 'm20_2', 'p17_1']
        ReadbackParameters = [
            {
                'Parameter': 'par0vd',
                'Xmin': -30,
                'Xmax': 30
            },
            {
                'Parameter': 'par1vd',
                'Xmin': 30,
                'Xmax': 100
            },
            {
                'Parameter': 'par0va',
                'Xmin': -30,
                'Xmax': 30
            },
            {
                'Parameter': 'par1va',
                'Xmin': 0,
                'Xmax': 100
            },
            {
                'Parameter': 'par0rbia',
                'Xmin': -20,
                'Xmax': 50
            },
            {
                'Parameter': 'par1rbia',
                'Xmin': -1,
                'Xmax': 3,
            },
            {
                'Parameter': 'par0tbia',
                'Xmin': 0,
                'Xmax': 10
            },
            {
                'Parameter': 'par1tbia',
                'Xmin': 0,
                'Xmax': 1
            },
            {
                'Parameter': 'par2tbia',
                'Xmin': -0.001,
                'Xmax': 0.001
            },
            {
                'Parameter': 'par0ia',
                'Xmin': -50,
                'Xmax': 50
            },
            {
                'Parameter': 'par1ia',
                'Xmin': 0,
                'Xmax': 1
            },
        ]

        self.SubPages.append({
            "InitialAttributes" : {
                "Sections": ["BumpBonding", "DeadPixel", "PerformanceParameters", "DACs", "IVCurves", "Readback", "HighRate", "VcalCalibration", "ReadoutErrors"],
                "DateBegin": self.Attributes['DateBegin'],
                "DateEnd": self.Attributes['DateEnd'],
            }, 
            "Key": "Section",
            "Module": "SectionNavigation"
        })

        if self.Attributes['ShowWeeklyPlots']:
            self.SubPages.append(
                {
                    "Key": "GradingOverview",
                    "Module": "GradingOverview",
                    "InitialAttributes" : {
                        "StorageKey" : "GradingOverview",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    },
                }
            )
            if not self.singleSubtest or 'Statistics' in self.singleSubtest:
                self.SubPages.append(
                    {
                        "Key": "WeeklyProduction",
                        "Module": "WeeklyProduction",
                        "InitialAttributes" : {
                            "StorageKey" : "WeeklyProduction",
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        },
                    }
                )

                self.SubPages.append(
                    {
                        "Key": "CumulativeProductionGraph",
                        "Module": "CumulativeProductionGraph",
                        "InitialAttributes" : {
                            "StorageKey" : "CumulativeProductionGraph",
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        },
                    }
                )

                self.SubPages.append(
                    {
                        "Key": "CumulativeProductionGraph",
                        "Module": "CumulativeProductionGraph",
                        "InitialAttributes" : {
                            "StorageKey" : "CumulativeProductionGraphAB",
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "AddAB": True,
                        },
                    }
                )
            if not self.singleSubtest or 'ModuleList' in self.singleSubtest:
                self.SubPages.append(
                    {
                        "Key": "ModuleList",
                        "Module": "ModuleList",
                        "InitialAttributes" : {
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        },
                    }
                )
                self.SubPages.append(
                    {
                        "Key": "BBCorners",
                        "Module": "BBCorners",
                        "InitialAttributes" : {
                            "StorageKey" : "BBCorners",
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "Test": SingleMinus20TestName,
                        },
                    }
                )
                self.IncludeSorttable = True

            if not self.singleSubtest or 'ModuleFailureOverview' in self.singleSubtest:
                Offset = 0
                NumModulesToShow = NumModules

                while (NumModulesToShow > 0):
                    self.SubPages.append(
                        {
                            "Key": "ModuleFailuresOverview_%d"%Offset,
                            "Module": "ModuleFailuresOverview",
                            "InitialAttributes" : {
                                "StorageKey" : "ModuleFailuresOverview_%d"%Offset,
                                "DateBegin": self.Attributes['DateBegin'],
                                "DateEnd": self.Attributes['DateEnd'],
                                "NumModules": NumModulesMaxPerList,
                                "Offset": Offset,
                            },
                        }
                    )
                    NumModulesToShow -= NumModulesMaxPerList
                    Offset += NumModulesMaxPerList
                self.SumJSONFilesModules.append('ModuleFailuresOverview')

                self.SubPages.append(
                    {
                        "Key": "PrimaryFailureReason",
                        "Module": "PrimaryFailureReason",
                        "InitialAttributes" : {
                            "StorageKey" : "PrimaryFailureReason",
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        },
                    }
                )
        else:
            self.SubPages.append(
                {
                    "Key": "GradingOverview",
                    "Module": "GradingOverview",
                    "InitialAttributes" : {
                        "StorageKey" : "GradingOverview",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    },
                }
            )
            self.SubPages.append(
                {
                    "Key": "ModuleFailuresOverview",
                    "Module": "ModuleFailuresOverview",
                    "InitialAttributes" : {
                        "StorageKey" : "ModuleFailuresOverview",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                        "Width": 4,
                    },
                }
            )
            self.SubPages.append(
                {
                    "Key": "PrimaryFailureReason",
                    "Module": "PrimaryFailureReason",
                    "InitialAttributes" : {
                        "StorageKey" : "PrimaryFailureReason",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    },
                }
            )

            self.SubPages.append(
                {
                    "Key": "ModuleList",
                    "Module": "ModuleList",
                    "InitialAttributes" : {
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    },
                }
            )

        ### bump bonding ###
        if not self.singleSubtest or 'BumpBonding' in self.singleSubtest:
            self.SubPages.append({"InitialAttributes" : {"Anchor": "BumpBonding", "Title": "BumpBonding Defects"}, "Key": "Section","Module": "Section"})
            for Grade in ['All','A', 'B', 'C']:
                self.SubPages.append(
                    {
                        "Key": "BumpBondingOverlay_{Grade}".format(Grade = Grade),
                        "Module": "BumpBondingOverlay",
                        "InitialAttributes" : {
                            "Grade": "{Grade}".format(Grade = Grade),
                            "StorageKey" : "BumpBondingOverlay_{Grade}".format(Grade = Grade),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )
            for Grade in ['All','A', 'B', 'C']:
                self.SubPages.append(
                    {
                        "Key": "BumpBondingOverlay_{Grade}".format(Grade = Grade),
                        "Module": "BumpBondingOverlay",
                        "InitialAttributes" : {
                            "Grade": "{Grade}".format(Grade = Grade),
                            "StorageKey" : "BumpBondingOverlayX_{Grade}".format(Grade = Grade),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "Xray": True,
                        }
                    }
                )
            self.SubPages.append(
                {
                    "Key": "BumpBondingVsId",
                    "Module": "BumpBondingVsId",
                    "InitialAttributes" : {
                        "StorageKey" : "BumpBondingVsId",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )

        if self.singleSubtest and 'XrayMap' in self.singleSubtest:
            self.SubPages.append(
                {
                    "Key": "XrayMap",
                    "Module": "XrayMap",
                    "InitialAttributes" : {
                        "Target": "Zn",
                        "StorageKey" : "XrayMap_Zn",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )
            self.SubPages.append(
                {
                    "Key": "XrayMap",
                    "Module": "XrayMap",
                    "InitialAttributes" : {
                        "Target": "Mo",
                        "StorageKey" : "XrayMap_Mo",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )
            self.SubPages.append(
                {
                    "Key": "XrayMap",
                    "Module": "XrayMap",
                    "InitialAttributes" : {
                        "Target": "Ag",
                        "StorageKey" : "XrayMap_Ag",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )
            self.SubPages.append(
                {
                    "Key": "XrayMap",
                    "Module": "XrayMap",
                    "InitialAttributes" : {
                        "Target": "Sn",
                        "StorageKey" : "XrayMap_Sn",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )

        ### dead pixel clusters###
        if self.singleSubtest and 'DeadPixelClusters' in self.singleSubtest:
            self.SubPages.append({"InitialAttributes" : {"Anchor": "DefectClusters", "Title": "Defect Clusters"}, "Key": "Section","Module": "Section"})
            self.SubPages.append(
                {
                    "Key": "DeadPixelClusters",
                    "Module": "DeadPixelClusters",
                    "InitialAttributes" : {
                        "Test": SingleMinus20TestName,
                        "StorageKey" : "DeadPixelClusters",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )
            self.SubPages.append(
                {
                    "Key": "DeadPixelClustersP17",
                    "Module": "DeadPixelClusters",
                    "InitialAttributes" : {
                        "Test": "p17_1",
                        "StorageKey" : "DeadPixelClustersP17",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )
        ### dead pixels ###
        if not self.singleSubtest or 'DeadPixels' in self.singleSubtest:
            self.SubPages.append({"InitialAttributes" : {"Anchor": "DeadPixel", "Title": "Dead Pixels"}, "Key": "Section","Module": "Section"})
            for Grade in ['All','A', 'B', 'C']:
                self.SubPages.append(
                    {
                        "Key": "DeadPixelOverlay_{Grade}".format(Grade = Grade),
                        "Module": "DeadPixelOverlay",
                        "InitialAttributes" : {
                            "Test": SingleMinus20TestName,
                            "Grade": "{Grade}".format(Grade = Grade),
                            "StorageKey" : "DeadPixelOverlay_{Grade}".format(Grade = Grade),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )
        ### pixels with bad treshold ###
        if not self.singleSubtest or 'ThresholdDefects' in self.singleSubtest:
            self.SubPages.append({"InitialAttributes" : {"Anchor": "BadThreshold", "Title": "Pixels with bad threshold"}, "Key": "Section","Module": "Section"})
            for Grade in ['All','A', 'B', 'C']:
                self.SubPages.append(
                    {
                        "Key": "ThresholdDefectsOverlay_{Grade}".format(Grade = Grade),
                        "Module": "ThresholdDefectsOverlay",
                        "InitialAttributes" : {
                            "Test": SingleMinus20TestName,
                            "Grade": "{Grade}".format(Grade = Grade),
                            "StorageKey" : "ThresholdDefectsOverlay_{Grade}".format(Grade = Grade),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )
        ### pixels with too high or low gain ###
        if not self.singleSubtest or 'GainDefects' in self.singleSubtest:
            self.SubPages.append({"InitialAttributes" : {"Anchor": "BadGain", "Title": "Pixels with bad gain"}, "Key": "Section","Module": "Section"})
            for Grade in ['All','A', 'B', 'C']:
                self.SubPages.append(
                    {
                        "Key": "GainOverlay_{Grade}".format(Grade = Grade),
                        "Module": "GainOverlay",
                        "InitialAttributes" : {
                            "Test": SingleMinus20TestName,
                            "Grade": "{Grade}".format(Grade = Grade),
                            "StorageKey" : "GainOverlay_{Grade}".format(Grade = Grade),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        ### performance parameters ###
        if not self.singleSubtest or 'MeanNoise' in self.singleSubtest:
            self.SubPages.append({"InitialAttributes" : {"Anchor": "PerformanceParameters", "Title": "Performance Parameters per ROC"}, "Key": "Section","Module": "Section"})
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "MeanNoise_{Test}".format(Test = Test),
                        "Module": "MeanNoise",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "MeanNoise_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )
        if not self.singleSubtest or 'RelativeGainWidth' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "RelativeGainWidth_{Test}".format(Test = Test),
                        "Module": "RelativeGainWidth",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "RelativeGainWidth_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )
        if not self.singleSubtest or 'PedestalSpread' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "PedestalSpread_{Test}".format(Test = Test),
                        "Module": "PedestalSpread",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "PedestalSpread_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        if not self.singleSubtest or 'VcalThresholdWidth' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "VcalThresholdWidth_{Test}".format(Test = Test),
                        "Module": "VcalThresholdWidth",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "VcalThresholdWidth_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        ### per pixel ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "PerPixel", "Title": "Pixel-based quantities"}, "Key": "Section","Module": "Section"})
        
        if not self.singleSubtest or 'GainPerPixel' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "GainPerPixel_{Test}".format(Test = Test),
                        "Module": "GainPerPixel",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "GainPerPixel__{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        if not self.singleSubtest or 'PedestalPerPixel' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "PedestalPerPixel_{Test}".format(Test = Test),
                        "Module": "PedestalPerPixel",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "PedestalPerPixel__{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        if not self.singleSubtest or 'SCurveWidthPerPixel' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "SCurveWidthsPerPixel_{Test}".format(Test = Test),
                        "Module": "SCurveWidthsPerPixel",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "SCurveWidthsPerPixel__{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        if not self.singleSubtest or 'VcalThresholdTrimmedPerPixel' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "VcalThresholdTrimmedPerPixel_{Test}".format(Test = Test),
                        "Module": "VcalThresholdTrimmedPerPixel",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "VcalThresholdTrimmedPerPixel__{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        ### DACs ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "DACs", "Title": "DAC Parameters"}, "Key": "Section","Module": "Section"})
        TrimThresholds = ['', '35']
        DACs = ['caldel', 'phoffset', 'phscale', 'vana', 'vthrcomp', 'vtrim']
        if not self.singleSubtest or 'DACDistribution' in self.singleSubtest:
            for Test in TestsList:
                for Trim in TrimThresholds:
                    for DAC in DACs:
                        self.SubPages.append(
                            {
                                "Key": "DACDistribution_{Test}".format(Test = Test),
                                "Module": "DACDistribution",
                                "InitialAttributes" : {
                                    "Test": "{Test}".format(Test = Test),
                                    "Trim": "{Trim}".format(Trim = Trim),
                                    "DAC": "{DAC}".format(DAC = DAC),
                                    "Maximum": 256,
                                    "NBins": 256,
                                    "StorageKey" : "DACDistribution_{Test}_{DAC}_{Trim}".format(Test=Test, DAC=DAC,Trim=Trim),
                                    "DateBegin": self.Attributes['DateBegin'],
                                    "DateEnd": self.Attributes['DateEnd'],
                                }
                            }
                        )

        if not self.singleSubtest or 'DAC2D' in self.singleSubtest:
            for Test in TestsList:
                for Trim in TrimThresholds:
                    for DACX,DACY in [ ['vthrcomp', 'vtrim'], ['phscale', 'phoffset'], ['vana', 'vthrcomp'] ]:
                        self.SubPages.append(
                            {
                                "Key": "Dac2D_{Test}".format(Test = Test),
                                "Module": "Dac2D",
                                "InitialAttributes" : {
                                    "Test": "{Test}".format(Test = Test),
                                    "Trim": "{Trim}".format(Trim = Trim),
                                    "DACX": "{DACX}".format(DACX = DACX),
                                    "DACY": "{DACY}".format(DACY = DACY),
                                    "StorageKey" : "Dac2D_{Test}_{DACX}_{DACY}_{Trim}".format(Test=Test, DACX=DACX, DACY=DACY, Trim=Trim),
                                    "DateBegin": self.Attributes['DateBegin'],
                                    "DateEnd": self.Attributes['DateEnd'],
                                }
                            }
                        )

        ### TrimBits ###
        if not self.singleSubtest or 'TrimBits' in self.singleSubtest:
            for Test in TestsList:
                for Trim in TrimThresholds:
                    self.SubPages.append(
                        {
                            "Key": "DACDistribution_{Test}".format(Test = Test),
                            "Module": "DACDistribution",
                            "InitialAttributes" : {
                                "Test": "{Test}".format(Test = Test),
                                "Trim": "{Trim}".format(Trim = Trim),
                                "DAC": "{DAC}".format(DAC = "TrimBits_mu"),
                                "Maximum": 16,
                                "NBins": 64,
                                "StorageKey" : "DACDistribution_{Test}_{DAC}_{Trim}".format(Test=Test, DAC="TrimBits_mu",Trim=Trim),
                                "DateBegin": self.Attributes['DateBegin'],
                                "DateEnd": self.Attributes['DateEnd'],
                            }
                        }
                    )
                    self.SubPages.append(
                        {
                            "Key": "DACDistribution_{Test}".format(Test = Test),
                            "Module": "DACDistribution",
                            "InitialAttributes" : {
                                "Test": "{Test}".format(Test = Test),
                                "Trim": "{Trim}".format(Trim = Trim),
                                "DAC": "{DAC}".format(DAC = "TrimBits_sigma"),
                                "Maximum": 5,
                                "NBins": 64,
                                "StorageKey" : "DACDistribution_{Test}_{DAC}_{Trim}".format(Test=Test, DAC="TrimBits_sigma",Trim=Trim),
                                "DateBegin": self.Attributes['DateBegin'],
                                "DateEnd": self.Attributes['DateEnd'],
                            }
                        }
                    )

        self.SubPages.append({"InitialAttributes" : {"Anchor": "DACDSpread35", "Title": "DAC parameter spread per module - 35"}, "Key": "Section","Module": "Section"})

        if not self.singleSubtest or 'CalDelSpread' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "DACSpreadPerModule_CalDel_{Test}".format(Test = Test),
                        "Module": "DACSpreadPerModule",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "CalDelPerModule_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "JSONPath": ['CalDel', 'KeyValueDictPairs.json', 'caldelspread', 'Value'],
                            "HistogramMin": 0,
                            "HistogramMax": 100,
                            "NBins": 50,
                            "Title": "CalDel difference %s"%Test,
                        }
                    }
                )

        if not self.singleSubtest or 'PHScaleSpread' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "DACSpreadPerModule_PHScale_{Test}".format(Test = Test),
                        "Module": "DACSpreadPerModule",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "PHScalePerModule_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "JSONPath": ['PHScale', 'KeyValueDictPairs.json', 'phscalespread', 'Value'],
                            "HistogramMin": 0,
                            "HistogramMax": 100,
                            "NBins": 50,
                            "Title": "PHScale difference %s"%Test,
                        }
                    }
                )


        if not self.singleSubtest or 'PHOffsetSpread' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "DACSpreadPerModule_PHOffset_{Test}".format(Test = Test),
                        "Module": "DACSpreadPerModule",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "PHOffsetPerModule_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "JSONPath": ['PHOffset', 'KeyValueDictPairs.json', 'phoffsetspread', 'Value'],
                            "HistogramMin": 0,
                            "HistogramMax": 100,
                            "NBins": 50,
                            "Title": "PHOffset difference %s"%Test,
                        }
                    }
                )

        if not self.singleSubtest or 'VthrCompSpread' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "DACSpreadPerModule_VthrComp_{Test}".format(Test = Test),
                        "Module": "DACSpreadPerModule",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "VthrCompPerModule_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "JSONPath": ['VthrComp', 'KeyValueDictPairs.json', 'vthrcompspread', 'Value'],
                            "HistogramMin": 0,
                            "HistogramMax": 100,
                            "NBins": 50,
                            "Title": "VthrComp difference %s"%Test,
                        }
                    }
                )

        if not self.singleSubtest or 'VtrimSpread' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "DACSpreadPerModule_Vtrim_{Test}".format(Test = Test),
                        "Module": "DACSpreadPerModule",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "VtrimPerModule_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "JSONPath": ['Vtrim', 'KeyValueDictPairs.json', 'vtrimspread', 'Value'],
                            "HistogramMin": 0,
                            "HistogramMax": 100,
                            "NBins": 50,
                            "Title": "Vtrim difference %s"%Test,
                        }
                    }
                )

        if not self.singleSubtest or 'VanaSpread' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "DACSpreadPerModule_Vana_{Test}".format(Test = Test),
                        "Module": "DACSpreadPerModule",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "VanaPerModule_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "JSONPath": ['Vana', 'KeyValueDictPairs.json', 'vanaspread', 'Value'],
                            "HistogramMin": 0,
                            "HistogramMax": 100,
                            "NBins": 50,
                            "Title": "Vana difference %s"%Test,
                        }
                    }
                )

        ### Full test duration ###
        if not self.singleSubtest or 'Duration' in self.singleSubtest:
            self.SubPages.append(
                {
                    "Key": "Duration",
                    "Module": "Duration",
                    "InitialAttributes" : {
                        "StorageKey" : "Duration",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )

        ### IV ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "IVCurves", "Title": "IV Curves"}, "Key": "Section","Module": "Section"})
        if not self.singleSubtest or 'IV' in self.singleSubtest or 'LeakageCurrent' in self.singleSubtest:
            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "IVCurveOverlay_{Test}".format(Test = Test),
                        "Module": "IVCurveOverlay",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "IVCurveOverlay_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "LeakageCurrent_{Test}".format(Test = Test),
                        "Module": "LeakageCurrent",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "LeakageCurrent_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

            for Test in TestsList:
                self.SubPages.append(
                    {
                        "Key": "LeakageCurrentSlope_{Test}".format(Test = Test),
                        "Module": "LeakageCurrentSlope",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "LeakageCurrentSlope_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

            for Test in ['m20_1','m20_2']:
                self.SubPages.append(
                    {
                        "Key": "LeakageCurrentRatio_{Test}".format(Test = Test),
                        "Module": "LeakageCurrentRatio",
                        "InitialAttributes" : {
                            "Test": "{Test}".format(Test = Test),
                            "StorageKey" : "LeakageCurrentRatio_{Test}".format(Test = Test),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        ### Readback ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "Readback", "Title": "Readback"}, "Key": "Section","Module": "Section"})
        if not self.singleSubtest or 'Readback' in self.singleSubtest:
            for Test in TestsList:
                for Parameter in ReadbackParameters:
                    self.SubPages.append(
                        {
                            "Key": "ReadbackParameter_{Test}_{Parameter}".format(Test = Test, Parameter = Parameter['Parameter']),
                            "Module": "ReadbackParameter",
                            "InitialAttributes" : {
                                "Test": Test,
                                "Parameter": Parameter['Parameter'],
                                "Xmin": Parameter['Xmin'],
                                "Xmax": Parameter['Xmax'],
                                "StorageKey" : "ReadbackParameter_{Test}_{Parameter}".format(Test = Test, Parameter = Parameter['Parameter']),
                                "DateBegin": self.Attributes['DateBegin'],
                                "DateEnd": self.Attributes['DateEnd'],
                            }
                        }
                    )

        ### HR ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "HighRate", "Title": "HighRateTests"}, "Key": "Section","Module": "Section"})
        if not self.singleSubtest or 'HREfficiency' in self.singleSubtest:
            for Rate in [50, 120]:
                self.SubPages.append(
                    {
                        "Key": "Efficiency_{Rate}".format(Rate = Rate),
                        "Module": "Efficiency",
                        "InitialAttributes" : {
                            "Rate": "{Rate}".format(Rate = Rate),
                            "StorageKey" : "Efficiency_{Rate}".format(Rate = Rate),
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                        }
                    }
                )

        if not self.singleSubtest or 'HRNoise' in self.singleSubtest:
            self.SubPages.append(
                {
                    "Key": "XrayNoisePerPixel",
                    "Module": "XrayNoisePerPixel",
                    "InitialAttributes" : {
                        "StorageKey" : "XrayNoisePerPixel",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )

        ### Vcal Calibration ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "VcalCalibration", "Title": "Vcal Calibration"}, "Key": "Section","Module": "Section"})
        
        if not self.singleSubtest or 'VcalCalibration' in self.singleSubtest:
            self.SubPages.append(
                {
                    "Key": "VcalSlope",
                    "Module": "VcalSlope",
                    "InitialAttributes" : {
                        "StorageKey" : "VcalSlope_Spectrum",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )
            self.SubPages.append(
                {
                    "Key": "VcalOffset",
                    "Module": "VcalOffset",
                    "InitialAttributes" : {
                        "StorageKey" : "VcalOffset_Spectrum",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )


        ### Errors ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "ReadoutErrors", "Title": "Readout Errors", "Caption": "<i>First bin means <strong>no errors</strong> and last bin includes overflow.</i>"}, "Key": "Section", "Module": "Section"})
        if not self.singleSubtest or 'Errors' in self.singleSubtest:
            for ErrorType in ['nErrors', 'nWarnings', 'nCriticals', 'message_daqerror_count',
                              'message_datasize_count','message_deser400_count', 'message_eventid_count',
                              'message_missingevents_count', 'message_notokenpass_count', 'message_readback_count',
                              'message_tokenchain_count', 'message_usbtimeout_count']:
                continue
                self.SubPages.append(
                    {
                        "Key": "ErrorsVsFW",
                        "Module": "ErrorsVsFW",
                        "InitialAttributes" : {
                            "StorageKey" : "ErrorsVsFW_%s"%ErrorType,
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "ErrorType": ErrorType,
                        }
                    }
                )

            for ErrorType in ['nErrors', 'nWarnings', 'nCriticals', 'message_daqerror_count',
                              'message_datasize_count','message_deser400_count', 'message_eventid_count',
                              'message_missingevents_count', 'message_notokenpass_count', 'message_readback_count',
                              'message_tokenchain_count', 'message_usbtimeout_count']:
                self.SubPages.append(
                    {
                        "Key": "ErrorsVsId",
                        "Module": "ErrorsVsId",
                        "InitialAttributes" : {
                            "StorageKey" : "ErrorsVsId_%s"%ErrorType,
                            "DateBegin": self.Attributes['DateBegin'],
                            "DateEnd": self.Attributes['DateEnd'],
                            "ErrorType": ErrorType,
                        }
                    }
                )

    def GenerateOverview(self):
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        # for all plots that have been split into several boxes
        # merge the JSON files to simplify further processing of the data

        for SumJSONFilesModule in self.SumJSONFilesModules:
            print("merge JSON files for '%s'..."%SumJSONFilesModule)
            TotalJSONDict = {}
            for Page in [x for x in self.SubPages if x['Module'] == SumJSONFilesModule]:
                Path = self.GlobalOverviewPath + '/' + self.Attributes['BasePath'] + '/' + Page['InitialAttributes']['StorageKey'] + "/KeyValueDictPairs.json"

                with open(Path) as data_file:
                    JSONData = json.load(data_file)
                    TotalJSONDict.update(JSONData)
                    print("add file: %s"%Path)

            # create directory
            JsonFileDir = self.GlobalOverviewPath + '/' + self.Attributes['BasePath'] + '/' + SumJSONFilesModule
            JsonFileName = JsonFileDir + '/KeyValueDictPairs.json'
            try:
                os.mkdir(JsonFileDir)
            except:
                pass

            # save file
            try:
                f = open(JsonFileName, 'w')
                f.write(json.dumps(TotalJSONDict, sort_keys=True, indent=4, separators=(',', ': '), cls=SetEncoder))
                f.close()
                print("-"*100)
                print("-> written to %s"%JsonFileName)
            except:
                print("could not write json file: '%s'!"%JsonFileName)



        HTML = "<a href='%s'>%s</a><br />"%(self.GetStorageKey()+'/'+self.HTMLFileName, self.Attributes['Title'])
        return HTML