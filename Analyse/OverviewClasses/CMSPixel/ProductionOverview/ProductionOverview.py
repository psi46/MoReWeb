import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self, TestResultEnvironmentObject = 0):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.HTMLFileName = 'ProductionOverview.html'
        self.ImportPath = 'OverviewClasses.CMSPixel.ProductionOverview'
        self.SaveHTML = True

        self.SubPages.append(
            {
                "Key": "GradingOverview",
                "Module": "GradingOverview",
                "InitialAttributes" : {
                    "StorageKey" : "GradingOverview",
                },
            }
        )


        self.SubPages.append(
            {
                "Key": "WeeklyProduction",
                "Module": "WeeklyProduction",
                "InitialAttributes" : {
                    "StorageKey" : "WeeklyProduction",
                },
            }
        )

        self.SubPages.append(
            {
                "Key": "CumulativeProductionGraph",
                "Module": "CumulativeProductionGraph",
                "InitialAttributes" : {
                    "StorageKey" : "CumulativeProductionGraph",
                },
            }
        )

        self.SubPages.append(
            {
                "Key": "ModuleList",
                "Module": "ModuleList",
            }
        )

        for Grade in ['All','A', 'B', 'C']:
            self.SubPages.append(
                {
                    "Key": "BumpBondingOverlay_{Grade}".format(Grade = Grade),
                    "Module": "BumpBondingOverlay",
                    "InitialAttributes" : {
                        "Grade": "{Grade}".format(Grade = Grade),
                        "StorageKey" : "BumpBondingOverlay_{Grade}".format(Grade = Grade),
                    }
                }
            )

        TestsList = ['m20_1', 'm20_2', 'p17_1']
        self.SubPages.append({"Key": "Dummy","Module": "Dummy"})

        for Test in TestsList:
            self.SubPages.append(
                {
                    "Key": "MeanNoise_{Test}".format(Test = Test),
                    "Module": "MeanNoise",
                    "InitialAttributes" : {
                        "Test": "{Test}".format(Test = Test),
                        "StorageKey" : "MeanNoise_{Test}".format(Test = Test),
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
                    }
                }
            )

        ### DACs ###
        self.SubPages.append({"Key": "Dummy","Module": "Dummy"})
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
                        }
                    }
                )

        ### Full test duration ###
        self.SubPages.append(
            {
                "Key": "Duration",
                "Module": "Duration",
            }
        )

        ### IV ###
        for Test in TestsList:
            self.SubPages.append(
                {
                    "Key": "IVCurveOverlay_{Test}".format(Test = Test),
                    "Module": "IVCurveOverlay",
                    "InitialAttributes" : {
                        "Test": "{Test}".format(Test = Test),
                        "StorageKey" : "IVCurveOverlay_{Test}".format(Test = Test),
                    }
                }
            )

    def GenerateOverview(self):
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return ""