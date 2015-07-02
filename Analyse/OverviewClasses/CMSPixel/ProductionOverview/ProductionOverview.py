import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self, TestResultEnvironmentObject = 0):
        if TestResultEnvironmentObject:
            self.TestResultEnvironmentObject = TestResultEnvironmentObject
        self.HTMLFileName = 'ProductionOverview.html'
        self.ImportPath = 'OverviewClasses.CMSPixel.ProductionOverview'
        self.NameSingle = 'ProductionOverview'
        self.Name = 'CMSPixel_%s'%self.NameSingle
        self.Attributes['StorageKey'] = self.NameSingle
        self.SaveHTML = True

        self.SubPages.append(
            {
                "Key": "ProductionOverviewPage_Total",
                "Module": "ProductionOverviewPage",
                "InitialAttributes" : {
                    "StorageKey" : "ProductionOverviewPage_Total",
                },
            }
        )


    def GenerateOverview(self):
        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return ""