import ROOT
import AbstractClasses

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
    	self.Name='CMSPixel_ProductionOverview_Dummy'
    	self.NameSingle='Dummy'
        self.DisplayOptions = {}
        self.SubPages = []

    def GenerateOverview(self):
        return "<div style='clear:both;'></div>"

