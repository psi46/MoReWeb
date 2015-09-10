import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self, TestResultEnvironmentObject = 0):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.HTMLFileName = 'ProductionOverview.html'
        self.ImportPath = 'OverviewClasses.CMSPixel.ProductionOverview.ProductionOverviewPage'

        self.NameSingle = 'ProductionOverviewPage'
        self.Name = 'CMSPixel_ProductionOverview_%s'%self.NameSingle

        self.SaveHTML = True

        TestsList = ['m20_1', 'm20_2', 'p17_1']

        self.SubPages.append({
            "InitialAttributes" : {
                "Sections": ["BumpBonding", "DeadPixel", "PerformanceParameters", "DACs", "IVCurves", "HighRate", "VcalCalibration"],
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

            self.SubPages.append(
                {
                    "Key": "ModuleFailuresOverview",
                    "Module": "ModuleFailuresOverview",
                    "InitialAttributes" : {
                        "StorageKey" : "ModuleFailuresOverview",
                        "DateBegin": self.Attributes['DateBegin'],
                        "DateEnd": self.Attributes['DateEnd'],
                    },
                }
            )
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

        for Test in TestsList:
            self.SubPages.append(
                {
                    "Key": "DeadPixelOverlay_{Test}".format(Test = Test),
                    "Module": "DeadPixelOverlay",
                    "InitialAttributes" : {
                        "Test": "{Test}".format(Test = Test),
                        "Grade": "All",
                        "StorageKey" : "DeadPixelOverlay_{Test}".format(Test = Test),
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

        HTML = "<a href='%s'>%s</a><br />"%(self.GetStorageKey()+'/'+self.HTMLFileName, self.Attributes['Title'])
        return HTML