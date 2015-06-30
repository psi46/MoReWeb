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
                "StorageKey" : "GradingOverview",
            }
        )


        self.SubPages.append(
            {
                "Key": "WeeklyProduction",
                "Module": "WeeklyProduction",
                "StorageKey" : "WeeklyProduction",
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

        for Test in ['m20_1', 'm20_2', 'p17_1']:
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

        for Test in ['m20_1', 'm20_2', 'p17_1']:
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

    def GenerateOverview(self):
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return ""