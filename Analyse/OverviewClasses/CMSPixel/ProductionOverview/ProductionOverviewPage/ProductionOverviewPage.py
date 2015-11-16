import ROOT
import AbstractClasses
import os, json

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self, TestResultEnvironmentObject = 0):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.HTMLFileName = 'ProductionOverview.html'
        self.ImportPath = 'OverviewClasses.CMSPixel.ProductionOverview.ProductionOverviewPage'

        self.NameSingle = 'ProductionOverviewPage'
        self.Name = 'CMSPixel_ProductionOverview_%s'%self.NameSingle

        self.SaveHTML = True

        Rows = self.FetchData()
        ModuleIDsList = self.GetModuleIDsList(Rows)
        NumModules = len(ModuleIDsList)
        NumModulesMaxPerList = 50

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
        ]

        self.SubPages.append({
            "InitialAttributes" : {
                "Sections": ["BumpBonding", "DeadPixel", "PerformanceParameters", "DACs", "IVCurves", "Readback", "HighRate", "VcalCalibration"],
                "DateBegin": self.Attributes['DateBegin'],
                "DateEnd": self.Attributes['DateEnd'],
            }, 
            "Key": "Section",
            "Module": "SectionNavigation"
        })

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

        if self.Attributes['ShowWeeklyPlots']:
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
                    "Key": "ModuleList",
                    "Module": "ModuleList",
                    "InitialAttributes" : {
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    },
                }
            )

            Offset = 0
            NumModulesToShow = NumModules

            while (NumModulesToShow > 0):
                self.SubPages.append(
                    {
                        "Key": "ModuleFailuresOverview",
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
        else:     
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
                    "Key": "ModuleList",
                    "Module": "ModuleList",
                    "InitialAttributes" : {
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    },
                }
            )



        ### bump bonding ###
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
        ### dead pixels ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "DeadPixel", "Title": "Dead Pixels"}, "Key": "Section","Module": "Section"})
        for Grade in ['All','A', 'B', 'C']:
            self.SubPages.append(
                {
                    "Key": "DeadPixelOverlay_{Grade}".format(Grade = Grade),
                    "Module": "DeadPixelOverlay",
                    "InitialAttributes" : {
                        "Test": "m20_2",
                        "Grade": "{Grade}".format(Grade = Grade),
                        "StorageKey" : "DeadPixelOverlay_{Grade}".format(Grade = Grade),
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )

        ### pixels with too high or low gain ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "BadGain", "Title": "Pixels with bad gain"}, "Key": "Section","Module": "Section"})
        for Grade in ['All','A', 'B', 'C']:
            self.SubPages.append(
                {
                    "Key": "GainOverlay_{Grade}".format(Grade = Grade),
                    "Module": "GainOverlay",
                    "InitialAttributes" : {
                        "Test": "m20_2",
                        "Grade": "{Grade}".format(Grade = Grade),
                        "StorageKey" : "GainOverlay_{Grade}".format(Grade = Grade),
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    }
                }
            )

        ### performance parameters ###
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

        #self.SubPages.append({"Key": "Dummy","Module": "Dummy"})

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

        #self.SubPages.append({"Key": "Dummy","Module": "Dummy"})

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

        #self.SubPages.append({"Key": "Dummy","Module": "Dummy"})

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

        ### TrimBits ###
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

        ### Full test duration ###
        self.SubPages.append(
            {
                "Key": "Duration",
                "Module": "Duration",
                "InitialAttributes" : {
                    "DateBegin": self.Attributes['DateBegin'],
                    "DateEnd": self.Attributes['DateEnd'],
                }
            }
        )

        ### IV ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "IVCurves", "Title": "IV Curves"}, "Key": "Section","Module": "Section"})
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

        ### Readback ###
        self.SubPages.append({"InitialAttributes" : {"Anchor": "Readback", "Title": "Readback"}, "Key": "Section","Module": "Section"})
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

    def GenerateOverview(self):
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)

        # for all plots that have been split into several boxes
        # merge the JSON files to simplify further processing of the data
        SumJSONFilesModules = ['ModuleFailuresOverview']
        for SumJSONFilesModule in SumJSONFilesModules:
            print("merge JSON files for '%s'..."%SumJSONFilesModule)
            TotalJSONDict = {}
            for Page in [x for x in self.SubPages if x['Key'] == SumJSONFilesModule]:
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